terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.7.2"
    }
  }
}

provider "random" {}

resource "random_password" "test" {
  length             = 16
  special            = true
  override_special = "!#$%^&*()-_=+[]{}<>.?:"
}

output "pw" {
  value = random_password.test.result
}