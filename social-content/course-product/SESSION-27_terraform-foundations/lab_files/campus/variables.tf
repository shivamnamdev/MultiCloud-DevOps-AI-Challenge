variable "region" {
  type    = string
  default = "us-east-1"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "Building size"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Use t3.micro, t3.small or t3.medium."
  }
}

variable "my_ip_cidr" {
  type        = string
  description = "Your public IP with /32, for SSH (find it with: curl -s https://checkip.amazonaws.com)"
  # No default on purpose: you must supply it, e.g. in terraform.tfvars
}

variable "ports" {
  type    = list(number)
  default = [80, 443]
}

variable "key_name" {
  type        = string
  default     = null
  description = "Name of an existing EC2 key pair, if you want to SSH in. Leave null to skip."
}
