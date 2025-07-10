data "aws_caller_identity" "current" {}

locals {
  opensearch_domain_name = "jaeger-logs"
  jaeger_domain_arn  = "arn:aws:es:${var.region}:${data.aws_caller_identity.current.account_id}:domain/${local.opensearch_domain_name}"
}

resource "aws_security_group" "opensearch" {
  name        = "opensearch-sg"
  description = "Allow access to OpenSearch from EKS"
  vpc_id      = aws_vpc.gsalegig_vpc.id

  ingress {
    description      = "Allow HTTPS from EKS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    security_groups  = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "opensearch-sg"
  }
}

resource "aws_opensearch_domain" "jaeger" {
  domain_name           = local.opensearch_domain_name
  engine_version        = "OpenSearch_2.11"

  cluster_config {
    instance_type = "t3.small.search"
    instance_count = 2
  }

  ebs_options {
    ebs_enabled = true
    volume_type = "gp3"
    volume_size = 20
  }

  vpc_options {
    subnet_ids         = [aws_subnet.gsalegig_private_subnet[0].id]
    security_group_ids = [aws_security_group.opensearch.id]
  }

  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      # Principal = {
      #   AWS = aws_iam_role.jaeger_irsa.arn
      # }
      Principal = "*",
      Action    = "es:*"
      # Resource  = "arn:aws:es:${var.region}:${data.aws_caller_identity.current.account_id}:domain/${local.opensearch_domain_name}/*"
      Resource = "${local.jaeger_domain_arn}/*"
    }]
  })

  advanced_options = {
    "rest.action.multi.allow_explicit_index" = "true"
  }

  node_to_node_encryption {
    enabled = true
  }

  encrypt_at_rest {
    enabled = true
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}

resource "kubernetes_config_map" "jaeger_config" {
  metadata {
    name      = "jaeger-opensearch"
    namespace = "monitoring"
  }

  data = {
    OPENSEARCH_URL = aws_opensearch_domain.jaeger.endpoint
  }

  depends_on = [
#    null_resource.generate_kubeconfig,
    kubernetes_namespace.monitoring
  ]
}