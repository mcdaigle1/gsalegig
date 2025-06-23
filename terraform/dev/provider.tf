provider "aws" {
  region = "us-west-1"
  profile = "Administrator-450287579526"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
     }
  }
}