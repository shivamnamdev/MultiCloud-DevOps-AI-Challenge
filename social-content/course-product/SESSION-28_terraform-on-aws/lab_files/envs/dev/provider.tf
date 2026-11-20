# Credentials come from AWS_PROFILE or AWS_* variables, never from this file.
provider "aws" {
  region = var.region
  default_tags {
    tags = { Project = "atithi-lab", Env = var.env }
  }
}
