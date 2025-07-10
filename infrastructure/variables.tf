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
