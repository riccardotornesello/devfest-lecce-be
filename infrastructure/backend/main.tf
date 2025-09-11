locals {
  env_vars = {
    GS_BUCKET_NAME       = var.bucket_name
    POSTGRES_DB          = var.db_name
    POSTGRES_USER        = var.db_user
    POSTGRES_PASSWORD    = var.db_password
    POSTGRES_HOST        = "/cloudsql/${var.db_connection_name}"
    POSTGRES_PORT        = 5432
    ALLOWED_HOSTS        = "*"
    CORS_ALLOWED_ORIGINS = "*"
    CSRF_TRUSTED_ORIGINS = "https://api.devfest.gdglecce.it"
  }
}



resource "google_cloud_run_v2_service" "be" {
  name                = "devfest-lecce-be"
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"


  template {
    service_account = google_service_account.runner.email

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [var.db_connection_name]
      }
    }

    containers {
      image = var.image

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



resource "google_cloud_run_v2_job" "be_job" {
  name                = "devfest-lecce-be-job"
  location            = var.region
  deletion_protection = false

  template {
    template {
      service_account = google_service_account.runner.email

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [var.db_connection_name]
        }
      }

      containers {
        image = var.image

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




resource "google_cloud_run_v2_service_iam_member" "be_invoker" {
  name     = google_cloud_run_v2_service.be.name
  location = google_cloud_run_v2_service.be.location
  role     = "roles/run.invoker"
  member   = "allUsers"
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

