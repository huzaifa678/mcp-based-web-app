output "instance_public_ip" {
  value = aws_instance.app.public_ip
}

output "instance_public_dns" {
  value = aws_instance.app.public_dns
}

output "private_key_pem" {
  value     = tls_private_key.ec2_key.private_key_pem
  sensitive = true
}

