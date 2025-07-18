resource "google_storage_bucket" "media" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "member" {
  bucket   = google_storage_bucket.media.name
  role     = "roles/storage.objectViewer"
  member   = "allUsers"
}
