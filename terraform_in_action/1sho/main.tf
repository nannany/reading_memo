provider "aws" {
  region = "ap-northeast-1"
}
resource "aws_instance" "helloworld" {
  ami = "ami-09ebacdc178ae23b7"
  instance_type = "t2.micro"
  tags = {
    Name = "HelloWorld"
  }
}
