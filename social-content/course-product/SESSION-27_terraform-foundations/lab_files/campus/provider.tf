# Real AWS. Credentials come from AWS_PROFILE or the AWS_* environment variables, never from this file.
provider "aws" {
  region = var.region
}
