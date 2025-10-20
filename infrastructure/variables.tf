# Terraform Variables for DevFest Lecce Backend Infrastructure
# These variables must be set in terraform.tfvars or passed via command line

variable "region" {
  description = "The Google Cloud region where resources will be deployed (e.g., europe-west1)"
  type        = string
  default     = "europe-west1"
}

variable "project" {
  description = "The Google Cloud project ID where resources will be created"
  type        = string
}

variable "repository_id" {
  description = "The Artifact Registry repository ID for storing Docker images"
  type        = string
}

variable "bucket_name" {
  description = "The name of the Cloud Storage bucket for media files and static assets"
  type        = string
}

variable "domain" {
  description = "The domain name for the backend API (used for SSL certificate)"
  type        = string
}

variable "repo_owner" {
  description = "The GitHub repository owner/organization name"
  type        = string
  default     = "riccardotornesello"
}

variable "repo_name" {
  description = "The GitHub repository name"
  type        = string
  default     = "devfest-lecce-be"
}

# Database Configuration
# You can either use Cloud SQL (managed) or an external database

variable "use_cloud_sql" {
  description = "Whether to create and use Cloud SQL instance. Set to false to use an external database."
  type        = bool
  default     = true
}

# Cloud SQL specific variables (only used if use_cloud_sql = true)
variable "db_password" {
  description = "The password for the PostgreSQL database user (required for both Cloud SQL and external DB)"
  type        = string
  sensitive   = true
}

# External database variables (only used if use_cloud_sql = false)
variable "external_db_host" {
  description = "The hostname or IP address of the external PostgreSQL database"
  type        = string
  default     = ""
}

variable "external_db_port" {
  description = "The port of the external PostgreSQL database"
  type        = number
  default     = 5432
}

variable "external_db_name" {
  description = "The name of the external PostgreSQL database"
  type        = string
  default     = "devfest_lecce_db"
}

variable "external_db_user" {
  description = "The username for the external PostgreSQL database"
  type        = string
  default     = "devfest"
}
