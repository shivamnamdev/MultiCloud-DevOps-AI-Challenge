variable "staging_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

module "dev" {
  source = "./modules/network"
  name   = "dev"
  cidr   = "10.10.0.0/16"
}

module "staging" {
  source = "./modules/network"
  name   = "staging"
  cidr   = var.staging_cidr
}

output "dev_subnets" {
  value = module.dev.public_subnet_ids
}

output "staging_subnets" {
  value = module.staging.public_subnet_ids
}
