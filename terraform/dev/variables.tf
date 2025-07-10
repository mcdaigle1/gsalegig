# variable "kubeconfig_path" {
#   description = "Path to the kubeconfig file"
#   type        = string
#   default     = "~/.kube/config"
# }

variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-west-1" 
}
