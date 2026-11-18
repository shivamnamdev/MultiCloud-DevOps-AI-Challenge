# Practice without an AWS account: a local AWS emulator (see the guide).
# Copy this over provider.tf in the folder you are working in.
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints {
    ec2 = "http://localhost:4566"
    s3  = "http://localhost:4566"
    sts = "http://localhost:4566"
    iam = "http://localhost:4566"
  }
  default_tags {
    tags = { Owner = "atithi" }
  }
}
