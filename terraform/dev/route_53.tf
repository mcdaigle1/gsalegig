data "aws_route53_zone" "gsalegig" {
  name = "gsalegig.com"
}

resource "aws_route53_record" "api_cname" {
  zone_id = aws_route53_zone.gsalegig.id
  name    = "api.gsalegig.com"
  type    = "CNAME"
  ttl     = 300
  records = ["a451aba1beded4476b3fadff91dbf950-2089974327.us-west-1.elb.amazonaws.com."]
}