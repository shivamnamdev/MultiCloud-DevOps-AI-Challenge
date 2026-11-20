locals {
  name = "atithi-${var.env}"
}

module "network" {
  source = "./modules/network"
  name   = local.name
  cidr   = "10.30.0.0/16"
  azs    = var.azs
}

module "alb" {
  source     = "./modules/alb"
  name       = local.name
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.public_subnet_ids
}

module "compute" {
  source        = "./modules/compute"
  name          = local.name
  vpc_id        = module.network.vpc_id
  subnet_ids    = module.network.private_subnet_ids
  alb_sg_id     = module.alb.sg_id
  tg_arn        = module.alb.tg_arn
  instance_type = var.instance_type
}

module "database" {
  source         = "./modules/database"
  name           = local.name
  vpc_id         = module.network.vpc_id
  subnet_ids     = module.network.private_subnet_ids
  app_sg_id      = module.compute.sg_id
  instance_class = var.db_instance_class
  multi_az       = var.multi_az
}

output "alb_dns_name" {
  value = module.alb.dns_name
}
output "db_endpoint" {
  value = module.database.endpoint
}
output "db_secret_arn" {
  value = module.database.secret_arn
}
