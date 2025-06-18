variable "environment" {
  description = "Environment name (e.g., test, staging, prod)"
  type        = string
  default     = "test"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "image_tag" {
  description = "Docker image tag for the application"
  type        = string
  default     = "latest"
}

variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
  sensitive   = true
}

variable "client_id" {
  description = "Azure service principal client ID"
  type        = string
  sensitive   = true
}

variable "client_secret" {
  description = "Azure service principal client secret"
  type        = string
  sensitive   = true
}
