# compute ami
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# keypair creation

resource "tls_private_key" "exposed_credentials" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "group18" {
  key_name   = "group18-${local.date}"
  public_key = tls_private_key.exposed_credentials.public_key_openssh
}

# Save the private key to a file
resource "local_file" "private_key" {
  content  = tls_private_key.exposed_credentials.private_key_pem
  file_permission = "0400"
  filename = "group18-${local.date}.pem"
}

# Save the private key to a file
resource "local_file" "public_key" {
  content  = tls_private_key.exposed_credentials.public_key_openssh
  file_permission = "0400"
  filename = "group18-${local.date}.pub"
}

# Create the IAM role
resource "aws_iam_role" "group18" {
  name               = "group18-${local.date}-Role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
  path = local.path
}

# Define the trust relationship for the IAM role
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# Get the SecretsManagerReadWrite policy
data "aws_iam_policy" "secrets_manager_read_write" {
  arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

# Attach the SecretsManagerReadWrite policy to the IAM role
resource "aws_iam_role_policy_attachment" "attach_secrets_manager" {
  role       = aws_iam_role.group18.name
  policy_arn = data.aws_iam_policy.secrets_manager_read_write.arn
}

# Get the AmazonSSMFullAccess policy
data "aws_iam_policy" "ssm_full_access" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMFullAccess"
}

# Attach the SecretsManagerReadWrite policy to the IAM role
# SECURITY ISSUE: Should narrow scope
resource "aws_iam_role_policy_attachment" "attach_ssm_full_access" {
  role       = aws_iam_role.group18.name
  policy_arn = data.aws_iam_policy.ssm_full_access.arn
}

# Get the AmazonSSMManagedInstanceCore policy
data "aws_iam_policy" "ssm_managed_instance_core" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Attach the SecretsManagerReadWrite policy to the IAM role
resource "aws_iam_role_policy_attachment" "attach_ssm_managed_instance_core" {
  role       = aws_iam_role.group18.name
  policy_arn = data.aws_iam_policy.ssm_managed_instance_core.arn
}

# Get the AmazonSSMManagedInstanceCore policy
data "aws_iam_policy" "ssm_patch_association" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMPatchAssociation"
}

# Attach the SecretsManagerReadWrite policy to the IAM role
resource "aws_iam_role_policy_attachment" "attach_ssm_patch_asssociation" {
  role       = aws_iam_role.group18.name
  policy_arn = data.aws_iam_policy.ssm_patch_association.arn
}

resource "aws_iam_instance_profile" "group18" {
  name = "group18-${local.date}-InstanceProfile"
  role = aws_iam_role.group18.name
}

resource "aws_security_group" "ssh_access" {
  name        = "group18-${local.date}"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Change this to your desired IP range
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "exposed_credentials" {
  count = var.numberOfCompute
  ami           = data.aws_ami.amazon_linux_2.image_id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.group18.key_name
  vpc_security_group_ids = [aws_security_group.ssh_access.id]
  iam_instance_profile = aws_iam_instance_profile.group18.name

  user_data = <<-EOF
    #!/bin/bash
    sudo adduser group-18-${count.index}-${local.date}
    sudo usermod -aG wheel group-18-${count.index}-${local.date}
    sudo usermod -aG wheel group-18-${count.index}-${local.date}
    sudo passwd -d group-18-${count.index}-${local.date}
  EOF

  tags = {
    Name = "compute-${count.index + 1}-${local.date}"
  }
}