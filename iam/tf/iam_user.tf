resource "aws_iam_user" "users" {
  count = var.numberOfUsers
  name  = "user-${count.index + 1}-${local.date}"
  path = local.path
}

output "user_names" {
  value       = [for user in aws_iam_user.users : user.name]
  description = "Names of the created IAM users"
}
