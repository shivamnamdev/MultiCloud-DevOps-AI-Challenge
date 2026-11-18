variable "name" {
  type        = string
  description = "Campus name"
}

variable "cidr" {
  type        = string
  description = "Campus CIDR"

  validation {
    condition     = can(cidrhost(var.cidr, 0))
    error_message = "cidr must be a valid CIDR such as 10.10.0.0/16."
  }
}

variable "public_subnet_count" {
  type    = number
  default = 2
}

variable "tags" {
  type    = map(string)
  default = {}
}
