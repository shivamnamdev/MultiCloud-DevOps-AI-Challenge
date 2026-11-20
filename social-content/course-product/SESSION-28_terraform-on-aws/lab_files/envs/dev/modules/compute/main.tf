# Ubuntu 24.04 image id, from Canonical's public parameter (no hard-coded ami id)
data "aws_ssm_parameter" "ubuntu" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}

resource "aws_security_group" "app" {
  name   = "${var.name}-app-sg"
  vpc_id = var.vpc_id
}

# Port 80 only from the load balancer's group, not from the world (Session 11)
resource "aws_vpc_security_group_ingress_rule" "from_alb" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = var.alb_sg_id
  from_port                    = 80
  to_port                      = 80
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.app.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_launch_template" "web" {
  name_prefix            = "${var.name}-web-"
  image_id               = data.aws_ssm_parameter.ubuntu.value
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.app.id]
  user_data = base64encode(<<-EOT
    #!/bin/bash
    apt-get update -y
    apt-get install -y nginx
    echo "<h1>Atithi Hotels: Book Now</h1><p>Served by $(hostname)</p>" > /var/www/html/index.html
  EOT
  )
  metadata_options {
    http_tokens = "required"
  }
  tag_specifications {
    resource_type = "instance"
    tags          = { Name = "${var.name}-web", Project = "atithi-lab" }
  }
}

resource "aws_autoscaling_group" "web" {
  name                      = "${var.name}-asg"
  min_size                  = 1
  max_size                  = 2
  desired_capacity          = 1
  vpc_zone_identifier       = var.subnet_ids
  target_group_arns         = [var.tg_arn]
  health_check_type         = "ELB"
  health_check_grace_period = 180
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  tag {
    key                 = "Project"
    value               = "atithi-lab"
    propagate_at_launch = true
  }
}
