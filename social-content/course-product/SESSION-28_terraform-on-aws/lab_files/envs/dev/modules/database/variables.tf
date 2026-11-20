variable "name" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "app_sg_id" { type = string }
variable "instance_class" { type = string }
variable "multi_az" { type = bool }
