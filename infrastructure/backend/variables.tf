variable "region" {
  type = string
}

variable "use_cloud_sql" {
  description = "Whether using Cloud SQL or external database"
  type        = bool
}

variable "db_password" {
  type = string
}

variable "db_name" {
  type = string
}

variable "db_user" {
  type = string
}

variable "db_host" {
  type = string
}

variable "db_port" {
  type = number
}

variable "db_connection_name" {
  description = "Cloud SQL connection name (only used if use_cloud_sql is true)"
  type        = string
}

variable "bucket_name" {
  type = string
}

variable "image" {
  type = string
}
