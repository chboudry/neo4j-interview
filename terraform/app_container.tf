# App Container Instance - Deploy this after image is pushed to ACR
resource "azurerm_container_group" "app" {
  name                = "aci-app-${var.environment}"
  location            = azurerm_resource_group.neo4j_interview.location
  resource_group_name = azurerm_resource_group.neo4j_interview.name
  ip_address_type     = "Public"
  dns_name_label      = "app-${var.environment}-${random_string.suffix.result}"
  os_type             = "Linux"

  image_registry_credential {
    server   = azurerm_container_registry.neo4j_interview.login_server
    username = azurerm_container_registry.neo4j_interview.admin_username
    password = azurerm_container_registry.neo4j_interview.admin_password
  }

  container {
    name   = "fastapi-app"
    image  = "${azurerm_container_registry.neo4j_interview.login_server}/neo4j-interview-app:${var.image_tag}"
    cpu    = "1"
    memory = "1.5"

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      NEO4J_URI      = "bolt://${azurerm_container_group.neo4j.fqdn}:7687"
      NEO4J_USERNAME = "neo4j"
      NEO4J_PASSWORD = "password"
      NEO4J_DATABASE = "neo4j"
    }
  }

  depends_on = [azurerm_container_group.neo4j]

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}
