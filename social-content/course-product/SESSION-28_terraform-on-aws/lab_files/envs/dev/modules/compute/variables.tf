variable "name" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "alb_sg_id" { type = string }
variable "tg_arn" { type = string }
variable "instance_type" { type = string }
