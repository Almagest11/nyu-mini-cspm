provider "aws" {
  region = "us-east-1"
  # we assume the ~/.aws/config is configured for a profile `nyu`
  # we assume the ~/.aws/credentials is ocnfigured for a profile `nyu`
  profile = "nyu"
}
