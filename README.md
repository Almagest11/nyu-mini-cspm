# nyu-mini-cspm

## Requirements
* Python3
* AWS account
* Terraform
* Django
* Docker

## IAM setup
`cd iam`
`source ./bin/activate`
`cd setup`
`terraform apply`

## IAM Scanning
`cd iam`
`source ./bin/activate`
`cd rules`
`pthon3 scan.py`

## IAM Cleanup
`cd iam`
`source ./bin/activate`
`cd setup`
`terraform destroy`


## Django
`cd iam`
`source ./bin/activate`
`cd ../cspm`
`python manage.py runserver`


## Build Dockerfile
`docker build -t group18 .`

## Run the site
`docker run -p 8000:8000 group18`