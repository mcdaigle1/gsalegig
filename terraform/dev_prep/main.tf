resource "aws_s3_bucket" "terraform_state" {
  bucket = "gsalegig-terraform-state"
  lifecycle {
    prevent_destroy = true
  }
  tags = {
    Name        = "Terraform State"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_sse" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_base_locks" {
  name         = "terraform-base-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  lifecycle {
    prevent_destroy = true
  }
  tags = {
    Name        = "Terraform Base State Lock Table"
    Environment = "dev"
  }
}

resource "aws_dynamodb_table" "terraform_apps_locks" {
  name         = "terraform-apps-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  lifecycle {
    prevent_destroy = true
  }
  tags = {
    Name        = "Terraform Apps State Lock Table"
    Environment = "dev"
  }
}