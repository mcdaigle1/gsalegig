# The EKS nodes security group
locals {
  eks_node_sg_id = data.terraform_remote_state.base.outputs.node_security_group_id
}

resource "aws_security_group" "gsalegig_rds" {
  name        = "rds-aurora-sg"
  description = "Allow access to Aurora from EKS nodes"
  vpc_id      = data.terraform_remote_state.base.outputs.vpc_id

  ingress {
    description      = "MySQL from EKS nodes"
    from_port        = 3306
    to_port          = 3306
    protocol         = "tcp"
    security_groups  = [local.eks_node_sg_id]  # Allow from EKS worker nodes
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-aurora-sg"
  }
}

# Generate a random password
resource "random_password" "db_master_password" {
  length           = 16
  special          = true
  override_special = "!#$%^&*()-_=+[]{}<>.?:"
}

# Create the secret
resource "aws_secretsmanager_secret" "db_master_credentials" {
  name = "gsalegig/dev/master-db-credentials"
  recovery_window_in_days = 0
}

# Store the generated password in the secret
resource "aws_secretsmanager_secret_version" "db_master_credentials_version" {
  secret_id     = aws_secretsmanager_secret.db_master_credentials.id
  secret_string = jsonencode({
    master_username = "admin"
    master_password = random_password.db_master_password.result
  })
}

resource "aws_rds_cluster" "gsalegig_aurora" {
  cluster_identifier      = "gsalegig-aurora-cluster"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.11.2"
  master_username         = "admin"
  master_password         = random_password.db_master_password.result
  database_name           = "gsalegig"
  db_subnet_group_name    = aws_db_subnet_group.aurora.name
  vpc_security_group_ids  = [aws_security_group.gsalegig_rds.id]
  skip_final_snapshot     = true
}

resource "aws_rds_cluster_instance" "aurora_instances" {
  count              = 2
  identifier         = "aurora-instance-${count.index + 1}"
  cluster_identifier = aws_rds_cluster.gsalegig_aurora.id
  instance_class     = "db.r6g.large"
  engine             = aws_rds_cluster.gsalegig_aurora.engine
  engine_version     = aws_rds_cluster.gsalegig_aurora.engine_version
  publicly_accessible = false
}

resource "aws_db_subnet_group" "aurora" {
  name       = "aurora-subnet-group"
  subnet_ids = data.terraform_remote_state.base.outputs.private_subnet_ids
}