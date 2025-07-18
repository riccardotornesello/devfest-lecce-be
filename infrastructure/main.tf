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
