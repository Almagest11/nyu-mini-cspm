# create a first active access key on odd users
resource "aws_iam_access_key" "user_access_key" {
  count = floor(var.numberOfUsers / 2)
  user  = aws_iam_user.users[count.index * 2].name
}

# create a second active access key on odd users
resource "aws_iam_access_key" "user_access_key_2nd" {
  count = floor(var.numberOfUsers / 2)
  user  = aws_iam_user.users[count.index * 2].name
}

output "user_access_key_id" {
  value       = [for key in aws_iam_access_key.user_access_key : key.id]
}

output "user_access_key_secret" {
  value       = [for key in aws_iam_access_key.user_access_key : key.secret]
  sensitive = true
}

output "user_access_key_id2" {
  value       = [for key in aws_iam_access_key.user_access_key_2nd : key.id]
}

output "user_access_key_secret2" {
  value       = [for key in aws_iam_access_key.user_access_key_2nd : key.secret]
  sensitive = true
}

