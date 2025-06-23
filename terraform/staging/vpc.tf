# ----------------------------
# Create VPC and Subnets
# ----------------------------
resource "aws_vpc" "gsalegig_vpc" {
  cidr_block = "10.3.0.0/16"
  
  tags = {
    Name = "gsalegig_vpc"
  }
}

resource "aws_subnet" "gsalegig_public_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.gsalegig_vpc.id
    cidr_block            = cidrsubnet(aws_vpc.gsalegig_vpc.cidr_block, 8, count.index + 100)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
}

resource "aws_subnet" "gsalegig_private_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.gsalegig_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.gsalegig_vpc.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
  
  tags = {
   # Name = "gsalegig-private-subnet-${count.index}"
   Name = "gsalegig-private-subnet-${data.aws_availability_zones.available.names[count.index]}"
 }
}

data "aws_availability_zones" "available" {}

resource "aws_internet_gateway" "gsalegig-igw" {
 vpc_id = aws_vpc.gsalegig_vpc.id

 tags = {
   Name = "gsalegig-igw"
 }
}

resource "aws_eip" "gsalegig-nat-eip" {
  domain  = "vpc"
}

resource "aws_nat_gateway" "gsalegig-nat" {
  allocation_id = aws_eip.gsalegig-nat-eip.id
  subnet_id     = aws_subnet.gsalegig_public_subnet[0].id
  depends_on    = [aws_internet_gateway.gsalegig-igw]
}

resource "aws_route_table" "gsalegig-public-rt" {
  vpc_id = aws_vpc.gsalegig_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gsalegig-igw.id
  }
}

resource "aws_route_table_association" "gsalegig-public-rta" {
  subnet_id      = aws_subnet.gsalegig_public_subnet[0].id
  route_table_id = aws_route_table.gsalegig-public-rt.id
}

resource "aws_route_table" "gsalegig_private_rt" {
 vpc_id = aws_vpc.gsalegig_vpc.id

 route {
   cidr_block = "0.0.0.0/0"
   nat_gateway_id = aws_nat_gateway.gsalegig-nat.id
 }

 tags = {
   Name = "gsalegig_private_rt"
 }
}

resource "aws_route_table_association" "gsalegig_private_rta" {
 count          = 2
 subnet_id      = aws_subnet.gsalegig_private_subnet.*.id[count.index]
 route_table_id = aws_route_table.gsalegig_private_rt.id
}