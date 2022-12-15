resource "random_uuid" "this" {}

module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 4.0"
  publish = true

  function_name = "lambda-test-${random_uuid.this.result}"
  handler       = "index.lambda_handler"
  runtime       = "python3.8"

  source_path = [
        "${path.module}/../../src/index.py",
        {
          pip_requirements = true,
          pip_requirements = "${path.module}/../../src/requirements.txt",
          commands = ["pip install -r requirements.txt"]
        },
  ]
}
