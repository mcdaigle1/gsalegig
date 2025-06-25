resource "helm_release" "nginx_ingress" {
  name       = "ingress-nginx"
  namespace  = "ingress-nginx"
  create_namespace = true

  repository   = "https://kubernetes.github.io/ingress-nginx"
  chart        = "ingress-nginx"
  version      = "4.12.3" # use latest compatible with your k8s
  timeout      = 600 # 10m
  wait         = true
  force_update = true

  values = [file("${path.module}/nginx-values.yaml")]
}