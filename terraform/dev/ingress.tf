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

  depends_on = [
    module.eks
  ]

  values = [file("${path.module}/nginx-values.yaml")]
}

resource "kubernetes_ingress_v1" "gsalegig" {
  metadata {
    name      = "gsalegig-ingress"
    namespace = "default"

    annotations = {
      "nginx.ingress.kubernetes.io/ssl-redirect" = "false"
      "nginx.ingress.kubernetes.io/use-regex"    = "false"
    }
  }

  spec {
    ingress_class_name = "nginx"

    rule {
      host = "api.gsalegig.com"

      http {
        path {
          path     = "/"
          path_type = "Prefix"

          backend {
            service {
              name = "gsalegig-api-service"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }

  depends_on = [
    helm_release.nginx_ingress
  ]
}