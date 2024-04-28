# Create an S3 bucket to store CloudTrail logs
resource "aws_s3_bucket" "cloudtrail_bucket" {
  bucket        = "ct-group18-${local.date}" # Replace with your desired bucket name
  force_destroy = true
}

# Create a CloudTrail trail
resource "aws_cloudtrail" "example_trail" {
  name                          = "ct-group18-${local.date}"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_bucket.id
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  include_global_service_events = true
}