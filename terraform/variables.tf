variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}


variable "ami_id" {
  description = "Amazon Machine Image ID"
  type        = string
  default     = "ami-0e8459476fed2e23b"
}
