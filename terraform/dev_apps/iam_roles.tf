###################################################################
# GITHUB ACTIONS ROLES
###################################################################
resource "aws_iam_role" "github_actions_role" {
  name = "github-actions-ecr-push"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:mcdaigle1/gsalegig:ref:refs/heads/main"
        }
      }
    }]
  })
}

resource "aws_iam_policy" "ecr_push" {
  name = "GitHubActionsECRPush"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.ecr_push.arn
}

###################################################################
# JAEGER ROLES
###################################################################
data "aws_eks_cluster" "this" {
  name = "gsalegig_eks_cluster"
}

data "aws_eks_cluster_auth" "this" {
  name = data.aws_eks_cluster.this.name
}

resource "aws_iam_role_policy" "jaeger_opensearch" {
  name = "JaegerToOpenSearchPolicy"
  role = aws_iam_role.jaeger_irsa.name
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "es:ESHttpPut",
          "es:ESHttpPost"
        ],
        "Resource": "${aws_opensearch_domain.jaeger.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role" "jaeger_irsa" {
  name = "jaeger-irsa-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = data.terraform_remote_state.base.outputs.oidc_provider_arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "${replace(data.terraform_remote_state.base.outputs.oidc_provider_url, "https://", "")}:sub" = "system:serviceaccount:monitoring:jaeger"
          }
        }
      }
    ]
  })
}