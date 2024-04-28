import json
import boto3
import sys
import time

PATH_PREFIX = "/group/18/final/"

global session

def list_ec2(client) :
    results = {}
    result = client.describe_instances( Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
    ])
    for reservation in result["Reservations"]:
        for instance in reservation["Instances"]:
            results[instance["InstanceId"]] = [tag["Value"] for tag in instance["Tags"] if tag["Key"] == "Name"][0] if "Tags" in instance else "<Unknown>"
    return results

def discover_exposure(client, ec2):
    findings = []
    if 0 == len([*ec2]):
        return findings
        
    response = client.send_command(
        InstanceIds = [*ec2],
        DocumentVersion = "1",
        DocumentName = "AWS-RunShellScript",
        Parameters = {
            "commands": [
                "#!/bin/bash",
                "# Script looks for users configured with a bash shell. It loops through these users and checks to see if they have an empty password and are wheel group members.",
                "# If the user satisfies both criteria, the script sets a complex random password and sends the password to AWS Secrets Manager.",
                "ssh_users=\"$(cat /etc/passwd | grep '/bin/bash' | awk -F: '{print $1}')\"",
                "wheel_members=\"$(sudo lid -g wheel | awk -F\\( '{print $1}')\"",
                "empty_passwords=\"0\"",
                "for user in $ssh_users ;",
                "do",
                " pwd_check=\"$(sudo passwd --status $user | awk '{print $2}')\"",
                " if [[ $pwd_check == 'NP' ]] && [[ $(echo ${wheel_members[@]} | grep $user) ]] ; then",
                " empty_passwords=\"1\"",
                " echo -e \"Found the privileged user: $user with an empty password!\"",
                " fi",
                "done",
                "if [ $empty_passwords == '0' ] ; then",
                " echo \"No empty passwords found.\"",
                "fi"
            ],
            "workingDirectory":[""],
            "executionTimeout":["3600"]
        },
        TimeoutSeconds = 30,
        MaxConcurrency = "50",
        MaxErrors = "0"
    )
    #print(json.dumps(response, indent = 2, default=str))
    commandId = response["Command"]["CommandId"]

    response = client.list_command_invocations(CommandId = commandId)
    n = 1
    while(len(response["CommandInvocations"]) == 0 or 0 != len([True for ci in response["CommandInvocations"] if ci["Status"] in ["Pending", "InProgress"] ])):
        response = client.list_command_invocations(CommandId = commandId)
        time.sleep(n)
        n = n * 2
    #print(json.dumps(response, indent = 2, default=str))

    for instanceId in [*ec2]:
        response = client.get_command_invocation(CommandId = commandId, InstanceId = instanceId)
        findings.append({"instanceId": instanceId, "result": response["StandardOutputContent"], "issue": "No empty passwords found." not in response["StandardOutputContent"] })
        #print(json.dumps(response, indent = 2, default=str))
    return findings

def ops_status(client):
    response = client.describe_ops_items(
        OpsItemFilters=[
            {
                'Key': 'Status',
                'Values': [
                    'Open',
                    'InProgress'
                ],
                'Operator': 'Equal'
            }
        ]
    )
    #print(json.dumps(response, indent = 2, default=str))
    return response["OpsItemSummaries"]



def lambda_handler(event, context):
    if context is None:
        context = {}
    ssm = context.get('ssm')
    if ssm is None:
        print("client not supplied, creating client")
        ssm = boto3.client('ssm')

    ec2 = context.get("ec2")
    if ec2 is None:
        print("client not supplied, creating client")
        ec2 = boto3.client('ec2')

    instances = list_ec2(ec2)
    findings = discover_exposure(ssm, instances)
    ops = ops_status(ssm)
    return {"instances":instances, "findings": findings, "ops": ops}

def build_context():
    global session
    session = boto3.Session(profile_name='nyu')
    return {"ec2": session.client('ec2'), "ssm": session.client("ssm")}

if __name__ == "__main__":
    result = lambda_handler(None, build_context()) 
    print(json.dumps(result, indent = 2))
