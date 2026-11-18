output "public_ip" {
  value = aws_instance.web.public_ip
}

output "subnet_cidr" {
  value = aws_subnet.public.cidr_block
}
