resource "aws_lb" "nlb" {
  name               = "app-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = [aws_subnet.main.id]

  tags = {
    Name = "app-nlb"
  }
}

resource "aws_lb_target_group" "app_tg" {
  name     = "app-tg"
  port     = 80
  protocol = "TCP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group" "app_tg_https" {
  name     = "app-tg-https"
  port     = 443
  protocol = "TCP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "app_attachment" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.app.id
  port             = 80
}

resource "aws_lb_target_group_attachment" "app_attachment_https" {
  target_group_arn = aws_lb_target_group.app_tg_https.arn
  target_id        = aws_instance.app.id
  port             = 443
}

resource "aws_lb_listener" "app_listener" {
  load_balancer_arn = aws_lb.nlb.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

resource "aws_lb_listener" "app_listener_https" {
  load_balancer_arn = aws_lb.nlb.arn
  port              = 443
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg_https.arn
  }
}