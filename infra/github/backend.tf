terraform {
  backend "local" {
    path = "../../secrets/tf-state/github/terraform.tfstate"
  }
}
