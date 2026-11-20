variable "region" {
  type    = string
  default = "ap-south-1"
}
variable "env" {
  type    = string
  default = "dev"
}
variable "azs" {
  type    = list(string)
  default = ["ap-south-1a", "ap-south-1b"]
}
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}
variable "multi_az" {
  type    = bool
  default = false
}
variable "single_nat_gateway" {
  type        = bool
  default     = true
  description = "One NAT gateway for the whole campus (cheaper, one point of failure)."
}
