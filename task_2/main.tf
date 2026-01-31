terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

#######################
# Provider
#######################
provider "aws" {
  region = var.aws_region
}

#######################
# Variables
#######################
variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}

#######################
# S3 Bucket
#######################
resource "aws_s3_bucket" "artifact_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
}

#######################
# Upload model artifact
#######################
resource "aws_s3_object" "model_artifact" {
  bucket = aws_s3_bucket.artifact_bucket.id
  key    = "model/model.tar.gz"
  source = "model.tar.gz"

  depends_on = [aws_s3_bucket.artifact_bucket]
}

#######################
# IAM Role for SageMaker
#######################
resource "aws_iam_role" "sagemaker_role" {
  name = "sagemaker-execution-role-genmab"


  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "sagemaker.amazonaws.com" }
      Action   = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "sagemaker_policy" {
  role = aws_iam_role.sagemaker_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:*"]
        Resource = [
          aws_s3_bucket.artifact_bucket.arn,
          "${aws_s3_bucket.artifact_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

#######################
# SageMaker Model
#######################
resource "aws_sagemaker_model" "model" {
  name               = "example-model"
  execution_role_arn = aws_iam_role.sagemaker_role.arn

  primary_container {
  image          = "763104351884.dkr.ecr.us-east-2.amazonaws.com/pytorch-inference:2.1.0-cpu-py310-ubuntu20.04"
  model_data_url = "s3://${aws_s3_bucket.artifact_bucket.bucket}/${aws_s3_object.model_artifact.key}"
  }


  depends_on = [aws_s3_object.model_artifact]
}

#######################
# Endpoint Config
#######################
resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = "example-endpoint-config"

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.model.name
    instance_type          = "ml.m5.large"
    initial_instance_count = 1
  }
}

#######################
# Endpoint
#######################
resource "aws_sagemaker_endpoint" "endpoint" {
  name                 = "example-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_config.name
}

#######################
# Outputs
#######################
output "endpoint_name" {
  value = aws_sagemaker_endpoint.endpoint.name
}
