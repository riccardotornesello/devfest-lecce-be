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

resource "google_artifact_registry_repository" "my-repo" {
  depends_on = [google_project_service.artifactregistry]

  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "default" {
  depends_on = [google_project_service.run]

  name                = "devfest-lecce-backend"
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${google_artifact_registry_repository.my-repo.project}/${google_artifact_registry_repository.my-repo.name}/devfest-lecce-backend:latest"
    }
  }
}
