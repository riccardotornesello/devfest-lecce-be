terraform {}

provider "google" {
  project         = var.project
  region          = var.region
  request_timeout = "60s"
}

locals {
  env_vars = {
    GS_BUCKET_NAME       = google_storage_bucket.media.name
    POSTGRES_DB          = google_sql_database.database.name
    POSTGRES_USER        = google_sql_user.user.name
    POSTGRES_PASSWORD    = var.db_password
    POSTGRES_HOST        = "/cloudsql/${google_sql_database_instance.instance.connection_name}"
    POSTGRES_PORT        = 5432
    ALLOWED_HOSTS        = "*"
    CSRF_TRUSTED_ORIGINS = "https://*.run.app"
  }
}

resource "google_project_service" "artifactregistry" {
  project            = var.project
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}
resource "google_project_service" "cloudbuild" {
  project            = var.project
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}
resource "google_project_service" "run" {
  project            = var.project
  service            = "run.googleapis.com"
  disable_on_destroy = false
}
resource "google_project_service" "compute" {
  project            = var.project
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}
resource "google_project_service" "sqladmin" {
  project            = var.project
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "my-repo" {
  depends_on = [google_project_service.artifactregistry]

  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
}

resource "google_storage_bucket" "media" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true
}

resource "google_cloud_run_v2_service" "be" {
  depends_on = [google_project_service.run, google_project_service.compute, google_project_service.sqladmin]

  name                = "devfest-lecce-be"
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"


  template {
    service_account = google_service_account.runner.email

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.instance.connection_name]
      }
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}/devfest-lecce-backend:latest"

      ports {
        container_port = 8000
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }

      dynamic "env" {
        for_each = local.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "be_invoker" {
  name     = google_cloud_run_v2_service.be.name
  location = google_cloud_run_v2_service.be.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_job" "be-job" {
  depends_on = [google_project_service.run, google_project_service.compute, google_project_service.sqladmin]

  name                = "devfest-lecce-be-job"
  location            = var.region
  deletion_protection = false

  template {
    template {
      service_account = google_service_account.runner.email

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.instance.connection_name]
        }
      }

      containers {
        image = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}/devfest-lecce-backend:latest"

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }

        dynamic "env" {
          for_each = local.env_vars
          content {
            name  = env.key
            value = env.value
          }
        }
      }
      timeout = "60s"
    }
  }
}

resource "google_sql_database_instance" "instance" {
  name             = "devfest-lecce-db"
  region           = var.region
  database_version = "POSTGRES_17"
  settings {
    edition = "ENTERPRISE"
    tier    = "db-f1-micro"
  }

  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "devfest_lecce_db"
  instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "user" {
  name     = "devfest"
  instance = google_sql_database_instance.instance.name
  password = var.db_password
}

resource "google_service_account" "runner" {
  account_id = "gcf-devfest-lecce-be-runner"
}

resource "google_project_iam_member" "sql" {
  project = google_service_account.runner.project
  role    = "roles/cloudsql.editor"
  member  = "serviceAccount:${google_service_account.runner.email}"
}

resource "google_project_iam_member" "cloud_storage" {
  project = google_service_account.runner.project
  role    = "roles/storage.objectUser"
  member  = "serviceAccount:${google_service_account.runner.email}"
}

resource "google_storage_bucket_iam_member" "member" {
  provider = google
  bucket   = google_storage_bucket.media.name
  role     = "roles/storage.objectViewer"
  member   = "allUsers"
}
