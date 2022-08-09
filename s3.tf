# Create the Bucket
resource "aws_s3_bucket" "aws_inventory" {
  bucket = var.bucket_name

  tags = { Name = "${var.name-prefix}-s3" }
}

# Block all public access to the bucket and objects
resource "aws_s3_bucket_public_access_block" "aws_inventory" {
  bucket = aws_s3_bucket.aws_inventory.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}