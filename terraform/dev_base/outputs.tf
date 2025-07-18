output "oidc_provider_arn" {
  value = module.eks.oidc_provider_arn
}

output "oidc_provider_url" {
  value = module.eks.oidc_provider
}

output "vpc_id" {
  value = aws_vpc.gsalegig_vpc.id
}

output "node_security_group_id" {
  value = module.eks.node_security_group_id
}

output "private_subnet_ids" {
  value = [for s in aws_subnet.gsalegig_private_subnet : s.id]
}