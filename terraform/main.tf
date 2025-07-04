# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.0"
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "neo4j_interview" {
  name     = "rg-neo4j-interview-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
    ManagedBy   = "terraform"
  }
}

# Create a virtual network
resource "azurerm_virtual_network" "neo4j_interview" {
  name                = "vnet-neo4j-interview-${var.environment}"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.neo4j_interview.location
  resource_group_name = azurerm_resource_group.neo4j_interview.name

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}

# Create a subnet
resource "azurerm_subnet" "neo4j_interview" {
  name                 = "subnet-neo4j-interview-${var.environment}"
  resource_group_name  = azurerm_resource_group.neo4j_interview.name
  virtual_network_name = azurerm_virtual_network.neo4j_interview.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "aci-delegation"
    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# Create Network Security Group
resource "azurerm_network_security_group" "neo4j_interview" {
  name                = "nsg-neo4j-interview-${var.environment}"
  location            = azurerm_resource_group.neo4j_interview.location
  resource_group_name = azurerm_resource_group.neo4j_interview.name

  # Allow HTTP traffic for the app
  security_rule {
    name                       = "AllowHTTP"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow Neo4j HTTP traffic
  security_rule {
    name                       = "AllowNeo4jHTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "7474"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow Neo4j Bolt traffic
  security_rule {
    name                       = "AllowNeo4jBolt"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "7687"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}

# Associate Network Security Group to Subnet
resource "azurerm_subnet_network_security_group_association" "neo4j_interview" {
  subnet_id                 = azurerm_subnet.neo4j_interview.id
  network_security_group_id = azurerm_network_security_group.neo4j_interview.id
}

# Create Azure Container Registry
resource "azurerm_container_registry" "neo4j_interview" {
  name                = "acr${lower(replace(var.environment, "-", ""))}neo4j${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.neo4j_interview.name
  location            = azurerm_resource_group.neo4j_interview.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}

# Random string for unique naming
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Storage account for Neo4j data persistence
resource "azurerm_storage_account" "neo4j_interview" {
  name                     = "st${lower(replace(var.environment, "-", ""))}neo4j${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.neo4j_interview.name
  location                 = azurerm_resource_group.neo4j_interview.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Environment = var.environment
    Project     = "neo4j-interview"
  }
}

# File share for Neo4j data
resource "azurerm_storage_share" "neo4j_data" {
  name                 = "neo4j-data"
  storage_account_name = azurerm_storage_account.neo4j_interview.name
  quota                = 50
}
