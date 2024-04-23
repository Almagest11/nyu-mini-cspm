
resource "aws_iam_user" "admin_user" {
  name  = "user-admin-${local.date}"
  path = local.path
}

# Attach the AdministratorAccess policy to the user
data "aws_iam_policy" "admin_policy" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_user_policy_attachment" "admin_user_policy_attachment" {
  user       = aws_iam_user.admin_user.name
  policy_arn = data.aws_iam_policy.admin_policy.arn
}

output "admin_user" {
  value       = aws_iam_user.admin_user.name
  description = "Name of the created Admin IAM user"
}

