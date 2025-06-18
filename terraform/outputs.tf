output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.neo4j_interview.name
}

output "neo4j_fqdn" {
  description = "FQDN of the Neo4j container instance"
  value       = azurerm_container_group.neo4j.fqdn
}

output "neo4j_ip_address" {
  description = "IP address of the Neo4j container instance"
  value       = azurerm_container_group.neo4j.ip_address
}

output "app_fqdn" {
  description = "FQDN of the application container instance"
  value       = azurerm_container_group.app.fqdn
}

output "app_ip_address" {
  description = "IP address of the application container instance"
  value       = azurerm_container_group.app.ip_address
}

output "app_url" {
  description = "URL to access the application"
  value       = "http://${azurerm_container_group.app.fqdn}:8000"
}

output "neo4j_browser_url" {
  description = "URL to access Neo4j Browser"
  value       = "http://${azurerm_container_group.neo4j.fqdn}:7474"
}

output "container_registry_login_server" {
  description = "Login server for the container registry"
  value       = azurerm_container_registry.neo4j_interview.login_server
}

output "container_registry_admin_username" {
  description = "Admin username for the container registry"
  value       = azurerm_container_registry.neo4j_interview.admin_username
  sensitive   = true
}

output "container_registry_admin_password" {
  description = "Admin password for the container registry"
  value       = azurerm_container_registry.neo4j_interview.admin_password
  sensitive   = true
}
