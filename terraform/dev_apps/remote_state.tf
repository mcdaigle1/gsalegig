data "terraform_remote_state" "base" {
  backend = "s3"
  config = {
    bucket = "gsalegig-terraform-state"     
    key    = "dev/base/terraform.tfstate"         
    region = "us-west-1"
  }
}