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

resource "google_artifact_registry_repository" "my-repo" {
  depends_on = [google_project_service.artifactregistry]

  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
}
