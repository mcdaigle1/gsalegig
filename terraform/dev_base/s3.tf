# the S3 backend is defined in the terraform/db_backend directory and is created separately
# from application environment

terraform {
  backend "s3" {
    bucket         = "gsalegig-terraform-state"
    key            = "dev/base/terraform.tfstate"
    region         = "us-west-1"
    dynamodb_table = "terraform-base-locks"
    encrypt        = true
  }
}