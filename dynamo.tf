# Create the DynamoDB Table and Partition key
resource "aws_dynamodb_table" "AWS_Inventory" {
  name         = "AWS_Inventory"
  hash_key     = "ID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "ID"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  tags = { Name = "${var.name-prefix}-dynamodb" }
}