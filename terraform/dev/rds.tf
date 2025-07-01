# The EKS nodes security group
locals {
  eks_node_sg_id = module.eks.node_security_group_id
}

resource "aws_security_group" "gsalegig_rds" {
  name        = "rds-aurora-sg"
  description = "Allow access to Aurora from EKS nodes"
  vpc_id      = aws_vpc.gsalegig_vpc.id

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

resource "aws_secretsmanager_secret" "gsalegig_aurora_master" {
  name = "/dev/gsalegig/aurora/master"
}

resource "aws_rds_cluster" "gsalegig_aurora" {
  cluster_identifier      = "gsalegig-aurora-cluster"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.11.2"
  master_username = jsondecode(aws_secretsmanager_secret_version.gsalegig_aurora_master.secret_string)["master_username"]
  master_password = jsondecode(aws_secretsmanager_secret_version.gsalegig_aurora_master.secret_string)["master_password"]
  database_name           = "gsalegig"
  db_subnet_group_name    = aws_db_subnet_group.aurora.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  skip_final_snapshot     = true
}

resource "aws_rds_cluster_instance" "aurora_instances" {
  count              = 2
  identifier         = "aurora-instance-${count.index + 1}"
  cluster_identifier = aws_rds_cluster.aurora.id
  instance_class     = "db.r6g.large"
  engine             = aws_rds_cluster.aurora.engine
  engine_version     = aws_rds_cluster.aurora.engine_version
  publicly_accessible = false
}

resource "aws_db_subnet_group" "aurora" {
  name       = "aurora-subnet-group"
  subnet_ids = [aws_subnet.gsalegig_private_subnet[0], aws_subnet.gsalegig_private_subnet[1]]
}