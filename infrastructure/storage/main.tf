# Cloud Storage Bucket
# Stores media files uploaded by users and static assets
resource "google_storage_bucket" "media" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false

  # Use uniform bucket-level access for consistent permissions
  uniform_bucket_level_access = true
}

# Grant public read access to the bucket
# This allows users to view uploaded media files
resource "google_storage_bucket_iam_member" "member" {
  bucket   = google_storage_bucket.media.name
  role     = "roles/storage.objectViewer"
  member   = "allUsers"
}
