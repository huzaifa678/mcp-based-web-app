terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.6.0"
}

provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "mcp-terraform-state-bucket-20334"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
