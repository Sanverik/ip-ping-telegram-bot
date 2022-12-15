resource "github_repository" "this" {
  name        = "ip-ping-telegram-bot"
  visibility  = "public"

  delete_branch_on_merge = true
  allow_squash_merge     = true
  allow_update_branch    = true
}

resource "github_repository_collaborator" "levovit" {
  repository = github_repository.this.name
  username   = "levovit"
  permission = "push"
}