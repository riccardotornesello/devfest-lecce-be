terraform {}

# Google Cloud Provider Configuration
# Manages all Google Cloud resources for the DevFest Lecce backend
provider "google" {
  project         = var.project
  region          = var.region
  request_timeout = "60s"
}

# Enable required Google Cloud APIs
# These APIs must be enabled before any resources can be created

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

# Artifact Registry repository for Docker images
# Stores the backend Docker images built by Cloud Build
resource "google_artifact_registry_repository" "my-repo" {
  depends_on = [google_project_service.artifactregistry]

  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
}

# Cloud Storage module
# Creates a bucket for media files and static assets
module "storage" {
  source      = "./storage"
  region      = var.region
  bucket_name = var.bucket_name
}

# Cloud SQL Database module
# Creates a PostgreSQL database instance for the application
# Only created if use_cloud_sql is true
module "db" {
  count = var.use_cloud_sql ? 1 : 0

  source        = "./db"
  region        = var.region
  password      = var.db_password
  instance_name = "devfest-lecce-db"
  db_name       = "devfest_lecce_db"
  user_name     = "devfest"
}

# Cloud Run Backend module
# Creates the Cloud Run service and job for the Django backend
module "backend" {
  source             = "./backend"
  region             = var.region
  use_cloud_sql      = var.use_cloud_sql
  db_password        = var.db_password
  db_name            = var.use_cloud_sql ? module.db[0].db_name : var.external_db_name
  db_user            = var.use_cloud_sql ? module.db[0].user_name : var.external_db_user
  db_host            = var.use_cloud_sql ? "/cloudsql/${module.db[0].connection_name}" : var.external_db_host
  db_port            = var.use_cloud_sql ? 5432 : var.external_db_port
  db_connection_name = var.use_cloud_sql ? module.db[0].connection_name : ""
  bucket_name        = module.storage.bucket_name
  image              = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}/devfest-lecce-backend:latest"
}

# HTTPS Load Balancer with SSL
# Provides a public HTTPS endpoint with automatic SSL certificate management
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

# Network Endpoint Group for Cloud Run
# Connects the load balancer to the Cloud Run service
resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  name                  = "serverless-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = module.backend.service_name
  }
}

# Cloud Build Service Account
# Used by Cloud Build to deploy and manage resources
resource "google_service_account" "cloudbuild_service_account" {
  account_id   = "cloudbuild-sa"
  display_name = "cloudbuild-sa"
  description  = "Cloud build service account"
}

# IAM permissions for Cloud Build service account
resource "google_project_iam_member" "act_as" {
  project = var.project
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.cloudbuild_service_account.email}"
}

resource "google_project_iam_member" "editor" {
  project = var.project
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.cloudbuild_service_account.email}"
}

resource "google_project_iam_member" "logs_writer" {
  project = var.project
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.cloudbuild_service_account.email}"
}

# Cloud Build Trigger
# Automatically deploys the backend on every push to the main branch
resource "google_cloudbuild_trigger" "build" {
  location        = var.region
  name            = "devfest-lecce-backend-build"
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.cloudbuild_service_account.id

  depends_on = [
    google_project_iam_member.act_as,
    google_project_iam_member.editor,
    google_project_iam_member.logs_writer
  ]

  # GitHub repository configuration
  github {
    owner = var.repo_owner
    name  = var.repo_name
    push {
      branch = "^main$"
    }
  }

  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"

  # Variables passed to cloudbuild.yaml
  substitutions = {
    _ARTIFACT_REGISTRY = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}"
    _SERVICE_REGION    = var.region
  }
}
