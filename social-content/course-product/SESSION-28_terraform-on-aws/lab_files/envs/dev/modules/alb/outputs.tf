output "dns_name" { value = aws_lb.this.dns_name }
output "tg_arn" { value = aws_lb_target_group.web.arn }
output "sg_id" { value = aws_security_group.alb.id }
