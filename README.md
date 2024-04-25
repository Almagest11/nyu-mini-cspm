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
`python manage.py collectstatic --noinput`
`python manage.py runserver`


## Build Dockerfile
`docker build -t group18 .`

## Run the site
`docker run -p 8000:8000 group18`

## Build and Run
`docker build -t group18 . && docker run -p 8000:8000 group18`

## UI builder
https://builder.creative-tim.com/builder/project-Lt73J8WX4hiAYzjO0yFC6n1rXoXo3DpQSis

## Icon Lookup
https://fonts.google.com/icons?selected=Material+Icons+Round:password:&icon.query=key&icon.set=Material+Icons&icon.style=Rounded

## NYU Logos
https://www.nyu.edu/employees/resources-and-services/media-and-communications/nyu-brand-guidelines/designing-in-our-style/nyu-logos-and-university-seal/using-logos-and-lockups.html