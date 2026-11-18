terraform {
  required_version = ">= 1.10"
  required_providers {
    terraform = { source = "terraform.io/builtin/terraform" }
  }
}

resource "terraform_data" "slow" {
  provisioner "local-exec" {
    command = "sleep 25"
  }
}
