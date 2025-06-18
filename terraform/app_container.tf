# Neo4j Container Instance - Deploy this with the app
resource "azurerm_container_group" "neo4j" {
  name                = "aci-neo4j-${var.environment}"
  location            = azurerm_resource_group.neo4j_interview.location
  resource_group_name = azurerm_resource_group.neo4j_interview.name
  ip_address_type     = "Public"
  dns_name_label      = "neo4j-${var.environment}-${random_string.suffix.result}"
  os_type             = "Linux"

  container {
    name   = "neo4j"
    image  = "${azurerm_container_registry.neo4j_interview.login_server}/neo4j:5.13-community"
    cpu    = "1"
    memory = "2"

    ports {
      port     = 7474
      protocol = "TCP"
    }

    ports {
      port     = 7687
      protocol = "TCP"
    }

    environment_variables = {
      NEO4J_AUTH                      = "neo4j/password"
      NEO4J_PLUGINS                   = "[\"apoc\", \"graph-data-science\"]"
      NEO4J_dbms_security_procedures_unrestricted = "apoc.*,gds.*"
      NEO4J_dbms_security_procedures_allowlist    = "apoc.*,gds.*"
    }

    volume {
      name       = "neo4j-data"
      mount_path = "/data"
      share_name = azurerm_storage_share.neo4j_data.name
      storage_account_name = azurerm_storage_account.neo4j_interview.name
      storage_account_key  = azurerm_storage_account.neo4j_interview.primary_access_key
    }
  }

  image_registry_credential {
    server   = azurerm_container_registry.neo4j_interview.login_server
    username = azurerm_container_registry.neo4j_interview.admin_username
    password = azurerm_container_registry.neo4j_interview.admin_password
  }

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}

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
    name   = "fullstack-app"
    image  = "${azurerm_container_registry.neo4j_interview.login_server}/neo4j-interview-app:${var.image_tag}"
    cpu    = "2"
    memory = "3"

    ports {
      port     = 8000
      protocol = "TCP"
    }

    ports {
      port     = 3000
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
