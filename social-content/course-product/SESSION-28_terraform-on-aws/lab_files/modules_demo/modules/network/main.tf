resource "aws_vpc" "this" {
  cidr_block = var.cidr
  tags       = merge(var.tags, { Name = var.name })
}

resource "aws_subnet" "public" {
  count      = var.public_subnet_count
  vpc_id     = aws_vpc.this.id
  cidr_block = cidrsubnet(var.cidr, 8, count.index)
  tags       = merge(var.tags, { Name = "${var.name}-public-${count.index}" })
}
