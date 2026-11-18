resource "aws_security_group" "web" {
  name        = "web-guard"
  description = "Web door guard"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
