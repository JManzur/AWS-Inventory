data "aws_iam_policy_document" "policy_source" {
  statement {
    sid    = "CloudWatchAccess"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    sid    = "EC2Permissions"
    effect = "Allow"
    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeAvailabilityZones",
      "ec2:DescribeRegions"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "PutObjectS3"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "${aws_s3_bucket.aws_inventory.arn}",
      "${aws_s3_bucket.aws_inventory.arn}/aws_inventory/*"
    ]
  }

  statement {
    sid    = "RDSPermissions"
    effect = "Allow"
    actions = [
      "rds:DescribeDBInstances"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "CrossAccountPermissions"
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    resources = var.Roles_List
  }
}

data "aws_iam_policy_document" "role_source" {
  statement {
    sid    = "LambdaAssumeRole"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# IAM Policy
resource "aws_iam_policy" "policy" {
  name        = "AWS_Inventory_Policy"
  path        = "/"
  description = "AWS_Inventory Policy"
  policy      = data.aws_iam_policy_document.policy_source.json
  tags        = { Name = "${var.name-prefix}-policy" }
}

# IAM Role (Lambda execution role)
resource "aws_iam_role" "role" {
  name               = "AWS_Inventory_Role"
  assume_role_policy = data.aws_iam_policy_document.role_source.json
  tags               = { Name = "${var.name-prefix}-role" }
}

# Attach Role and Policy
resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}