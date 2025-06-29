data "aws_caller_identity" "current" {}

resource "aws_opensearch_domain" "jaeger" {
  domain_name           = "jaeger-logs"
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

  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        AWS = aws_iam_role.jaeger_irsa.arn
      }
      Action    = "es:*"
      Resource  = "${aws_opensearch_domain.jaeger.arn}/*"
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

resource "kubernetes_config_map" "jaeger_config" {
  metadata {
    name      = "jaeger-opensearch"
    namespace = "monitoring"
  }

  data = {
    OPENSEARCH_URL = aws_opensearch_domain.jaeger.endpoint
  }
}