data "aws_route53_zone" "primary" {
  name         = "gsalegig.com"
  private_zone = false 
}

resource "aws_route53_record" "api_cname" {
  zone_id = data.aws_route53_zone.primary.id
  name    = "api.gsalegig.com"
  type    = "CNAME"
  ttl     = 300
  records = [kubernetes_ingress_v1.gsalegig.status.0.load_balancer.0.ingress.0.hostname]
}