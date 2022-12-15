resource "random_uuid" "this" {}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"
  publish = true

  function_name = "lambda-test-${random_uuid.this.result}"
  handler       = "index.lambda_handler"
  runtime       = "python3.8"

  source_path = [
    {
      path = "${path.module}/../../src",
      pip_requirements = true
    }
  ]

  environment_variables = {
    BOT_TOKEN             = var.BOT_TOKEN
    CHANNEL_ID            = var.CHANNEL_ID
    TARGET_IP             = var.TARGET_IP
    KEY_VALUE_STORE_TOKEN = var.KEY_VALUE_STORE_TOKEN
  }
}

resource "aws_cloudwatch_event_rule" "this" {
  name                = "${module.lambda_function.lambda_function_name}-event-rule"
  description         = "This event will run according to a schedule for Lambda ${module.lambda_function.lambda_function_name}"
  schedule_expression = "rate(5 minutes)"

  tags = {}
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.this.arn
}

resource "aws_cloudwatch_event_target" "this" {
  rule = aws_cloudwatch_event_rule.this.name
  arn  = module.lambda_function.lambda_function_arn
}
