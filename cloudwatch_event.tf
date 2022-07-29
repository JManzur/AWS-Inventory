# IMPORTANT: All schedule CloudWatch events use UTC time (GMT +0)
#   23:00 UTC = 19:00 EST
#   12:50 UTC = 08:50 EST

# Event Rule to Trigger the AWS-Inventory
resource "aws_cloudwatch_event_rule" "aws-inventory-mon-fri" {
  name                = "aws-inventory-mon-fri"
  description         = "AWS-Inventory at 19:00 EST Monday to Friday"
  schedule_expression = "cron(0 23 ? * MON-FRI *)"
  is_enabled          = var.enable_event_rules
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.aws-inventory-mon-fri.name
  target_id = "lambda"
  arn       = aws_lambda_function.AWS_Inventory.arn
  input     = "{\"key\":\"value\"}"
}

resource "aws_lambda_permission" "lambda" {
  statement_id  = "AWS-Inventory-Trigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.AWS_Inventory.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.aws-inventory-mon-fri.arn
}