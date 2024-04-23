# create passwords on even users
resource "aws_iam_user_login_profile" "user_login_profile" {
  count = floor(var.numberOfUsers / 2)
  user = aws_iam_user.users[count.index * 2 + 1].name
}

output "user_login_profile" {
  value       = [for profile in aws_iam_user_login_profile.user_login_profile : profile.password]
  sensitive = true
}
