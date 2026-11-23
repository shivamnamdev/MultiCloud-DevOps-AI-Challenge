terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
  }
}

variable "subscription_id" { type = string }
variable "suffix"          { type = string }

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id      # required since azurerm 4.0
}

resource "azurerm_resource_group" "demo" {
  name     = "rg-atithi-tf"
  location = "centralindia"
  tags     = { Project = "atithi-lab", owner = "shivam" }
}

resource "azurerm_storage_account" "warehouse" {
  name                            = "atithitf${var.suffix}"
  resource_group_name             = azurerm_resource_group.demo.name
  location                        = azurerm_resource_group.demo.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = false
  min_tls_version                 = "TLS1_2"
  tags                            = azurerm_resource_group.demo.tags
}
