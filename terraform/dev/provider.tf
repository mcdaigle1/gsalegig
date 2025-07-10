provider "aws" {
  region = "us-west-1"
  profile = "Administrator-450287579526"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.44"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.13"
    }
  }

  required_version = ">= 1.3"
}

data "aws_eks_cluster_auth" "this" {
  name = module.eks.cluster_name
}

# probably should look at creating kubernetes provider deterministically so we don't have to 
# regenerate local .kube/config, like:
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.this.token
}
# provider "kubernetes" {
#   config_path = var.kubeconfig_path
# }

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    token                  = data.aws_eks_cluster_auth.this.token
  }
}

# provider "helm" {
#   kubernetes {
#     config_path = var.kubeconfig_path
#   }
# }