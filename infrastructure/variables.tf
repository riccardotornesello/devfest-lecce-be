variable "region" {
  description = "The Google Cloud region where the function will be deployed."
  type        = string
  default     = "europe-west1"
}

variable "project" {
  description = "The Google Cloud project ID."
  type        = string
}

variable "repository_id" {
  type = string
}

variable "bucket_name" {
  type = string
}

variable "db_password" {
  type = string
}

variable "domain" {
  type = string
}

variable "repo_owner" {
  type    = string
  default = "riccardotornesello"
}

variable "repo_name" {
  type    = string
  default = "devfest-lecce-be"
}
