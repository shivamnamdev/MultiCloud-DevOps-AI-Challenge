resource "aws_security_group" "db" {
  name   = "${var.name}-db-sg"
  vpc_id = var.vpc_id
}

# The database door opens only for the app's group (Session 13)
resource "aws_vpc_security_group_ingress_rule" "from_app" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = var.app_sg_id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db-subnets"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "this" {
  identifier                  = "${var.name}-db"
  engine                      = "postgres"
  instance_class              = var.instance_class
  allocated_storage           = 20
  storage_type                = "gp3"
  storage_encrypted           = true
  db_name                     = "ledger"
  username                    = "atithi_admin"
  manage_master_user_password = true # the password lives in Secrets Manager, never in state or code
  db_subnet_group_name        = aws_db_subnet_group.this.name
  vpc_security_group_ids      = [aws_security_group.db.id]
  publicly_accessible         = false
  multi_az                    = var.multi_az
  backup_retention_period     = 1
  deletion_protection         = false # PRACTICE ONLY. Use true for anything you care about, and set skip_final_snapshot = false.
  skip_final_snapshot         = true
}
