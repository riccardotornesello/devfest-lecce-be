output "connection_name" {
  value = google_sql_database_instance.instance.connection_name
}

output "user_name" {
  value = google_sql_user.user.name
}

output "db_name" {
  value = google_sql_database.database.name
}
