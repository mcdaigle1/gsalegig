###################################################################
# CLUSTER ROLES
###################################################################
# Node group IAM role
resource "aws_iam_role" "eks_node_role" {
  name = "eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach required managed policies
resource "aws_iam_role_policy_attachment" "worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role" "eks_cluster_role" {
  name = "gsalegig_eks_cluster-cluster-20250529174826744800000001"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = [
          "sts:TagSession",
          "sts:AssumeRole",
        ]
      }
    ]
  })

  tags = {
    "Environment" = "dev"
    "Terraform"   = "true"
  }
}

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
          Federated = module.eks.oidc_provider_arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "${replace(module.eks.oidc_provider, "https://", "")}:sub" = "system:serviceaccount:monitoring:jaeger"
          }
        }
      }
    ]
  })
}