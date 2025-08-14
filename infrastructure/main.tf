terraform {}

provider "google" {
  project         = var.project
  region          = var.region
  request_timeout = "60s"
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

module "storage" {
  source      = "./storage"
  region      = var.region
  bucket_name = var.bucket_name
}

module "db" {
  source        = "./db"
  region        = var.region
  password      = var.db_password
  instance_name = "devfest-lecce-db"
  db_name       = "devfest_lecce_db"
  user_name     = "devfest"
}

module "backend" {
  source             = "./backend"
  region             = var.region
  db_password        = var.db_password
  db_name            = module.db.db_name
  db_user            = module.db.user_name
  db_connection_name = module.db.connection_name
  bucket_name        = module.storage.bucket_name
  image              = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}/devfest-lecce-backend:latest"
}

module "lb-http" {
  source  = "terraform-google-modules/lb-http/google//modules/serverless_negs"
  version = "~> 12.0"

  name    = "devfest-lecce-http-lb"
  project = var.project

  ssl                             = true
  managed_ssl_certificate_domains = [var.domain]
  https_redirect                  = true

  backends = {
    default = {
      description = null
      groups = [
        {
          group = google_compute_region_network_endpoint_group.serverless_neg.id
        }
      ]
      enable_cdn = false

      iap_config = {
        enable = false
      }
      log_config = {
        enable = false
      }
    }
  }
}

resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  name                  = "serverless-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = module.backend.service_name
  }
}

resource "google_service_account" "cloudbuild_service_account" {
  account_id   = "cloudbuild-sa"
  display_name = "cloudbuild-sa"
  description  = "Cloud build service account"
}

resource "google_project_iam_member" "cloudbuild_service_account_editor" {
  project = var.project
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.cloudbuild_service_account.email}"
}

resource "google_project_iam_member" "cloudbuild_service_account_logs" {
  project = var.project
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.cloudbuild_service_account.email}"
}


resource "google_cloudbuild_trigger" "build" {
  location        = var.region
  name            = "devfest-lecce-backend-build"
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.cloudbuild_service_account.id

  github {
    owner = var.repo_owner
    name  = var.repo_name
    push {
      branch = "^main$"
    }
  }

  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"

  substitutions = {
    _ARTIFACT_REGISTRY = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}"
    _SERVICE_REGION    = var.region
  }
}
