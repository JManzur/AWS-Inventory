# Zip the lambda code
data "archive_file" "AWS_Inventory" {
  type        = "zip"
  source_dir  = "lambda_code/AWS_Inventory/"
  output_path = "output_lambda_zip/AWS_Inventory/AWS_Inventory.zip"
}

# Create lambda function
resource "aws_lambda_function" "AWS_Inventory" {
  filename      = data.archive_file.AWS_Inventory.output_path
  function_name = "AWS_Inventory"
  role          = aws_iam_role.role.arn
  handler       = "main_handler.lambda_handler"
  description   = "AWS resources inventory"
  tags          = { Name = "${var.name-prefix}-lambda" }

  # Prevent lambda recreation
  source_code_hash = filebase64sha256(data.archive_file.AWS_Inventory.output_path)

  environment {
    variables = {
      bucket_name = var.bucket_name
    }
  }
  runtime = "python3.9"
  timeout = "120"
}