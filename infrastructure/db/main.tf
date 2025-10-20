# Cloud SQL PostgreSQL Instance
# Managed database for the Django application
resource "google_sql_database_instance" "instance" {
  name             = var.instance_name
  region           = var.region
  database_version = "POSTGRES_17"
  settings {
    edition = "ENTERPRISE"
    tier    = "db-f1-micro"  # Free tier eligible instance
  }

  # Prevent accidental deletion of the database
  deletion_protection = true
}

# Database within the Cloud SQL instance
resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.instance.name
}

# Database user with credentials
resource "google_sql_user" "user" {
  name     = var.user_name
  instance = google_sql_database_instance.instance.name
  password = var.password
}
