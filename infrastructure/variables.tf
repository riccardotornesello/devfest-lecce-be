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

variable "db_password" {
  description = "The password for the PostgreSQL database user (use a strong password)"
  type        = string
  sensitive   = true
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
