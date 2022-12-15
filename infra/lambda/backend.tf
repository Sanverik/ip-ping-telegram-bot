terraform {
  backend "local" {
    path = "../../secrets/tf-state/lambda/terraform.tfstate"
  }
}
