module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.21.0" # or any stable 19.x you prefer

  cluster_name    = "gsalegig_eks_cluster"
  cluster_version = "1.33"

  enable_irsa = true
  cluster_endpoint_public_access = true

  vpc_id     = aws_vpc.gsalegig_vpc.id
  subnet_ids = aws_subnet.gsalegig_private_subnet[*].id

  eks_managed_node_groups = {
    general = {
      instance_types = ["t3.medium"]
      desired_size   = 2
      min_size       = 2
      max_size       = 3
      node_role_arn  = aws_iam_role.eks_node_role.arn
    }
  }

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

resource "null_resource" "generate_kubeconfig" {
  depends_on = [module.eks]

  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
  }
}