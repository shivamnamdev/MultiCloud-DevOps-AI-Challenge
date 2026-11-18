# Real AWS. Credentials come from AWS_PROFILE or AWS_* variables, never from this file.
provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = { Owner = "atithi" }
  }
}
