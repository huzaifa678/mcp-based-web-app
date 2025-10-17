data "aws_route53_zone" "main" {
  name         = var.domain_name   
  private_zone = false
}

resource "aws_route53_record" "app_alias" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.subdomain_name     
  type    = "A"

  alias {
    name                   = aws_lb.nlb.dns_name
    zone_id                = aws_lb.nlb.zone_id
    evaluate_target_health = true
  }
}