# Create the KMS Key
resource "aws_kms_key" "aws_inventory" {
  description             = "S3 Encryption Key"
  deletion_window_in_days = 15
  multi_region            = false
  tags                    = { Name = "${var.name-prefix}-kms-key" }
}

# Create the Bucket
resource "aws_s3_bucket" "aws_inventory" {
  bucket = var.bucket_name

  tags = { Name = "${var.name-prefix}-s3" }
}

# Enable Versioning on Bucket
resource "aws_s3_bucket_versioning" "aws_inventory" {
  bucket = aws_s3_bucket.aws_inventory.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Block all public access to the bucket and objects
resource "aws_s3_bucket_public_access_block" "aws_inventory" {
  bucket = aws_s3_bucket.aws_inventory.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enble Server Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "aws_inventory" {
  bucket = aws_s3_bucket.aws_inventory.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.aws_inventory.arn
      sse_algorithm     = "aws:kms"
    }
  }

  depends_on = [aws_kms_key.aws_inventory]
}