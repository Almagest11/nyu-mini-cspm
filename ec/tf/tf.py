import subprocess
import pathlib

def setup():
    cwd = pathlib.Path(__file__).parent.resolve()
    print("terraform init")
    output = subprocess.run(["terraform init"], shell=True, cwd=cwd, text=True)
    print(output)
    print("terraform apply")
    output = subprocess.run(["terraform apply -auto-approve"], shell=True, cwd=cwd, text=True)
    print(output)

def teardown():
    cwd = pathlib.Path(__file__).parent.resolve()
    print("terraform init")
    output = subprocess.run(["terraform init"], shell=True, cwd=cwd, text=True)
    print(output)
    print("terraform destroy")
    output = subprocess.run(["terraform destroy -auto-approve"], shell=True, cwd=cwd, text=True)
    print(output)
