import json
import boto3
import time

def remediate(instanceId, client):
    response = client.send_command(
        InstanceIds = [instanceId],
        DocumentVersion = "1",
        DocumentName = "AWS-RunShellScript",
        Parameters = {
            "commands": [
                "#!/bin/bash",
                "ssh_users=\"$(cat /etc/passwd | grep '/bin/bash' | awk -F: '{print $1}')\"",
                "wheel_members=\"$(sudo lid -g wheel | awk -F\\( '{print $1}')\"",
                "empty_passwords=\"0\"",
                "for user in $ssh_users ;",
                "do",
                " pwd_check=\"$(sudo passwd --status $user | awk '{print $2}')\"",
                " if [[ $pwd_check == 'NP' ]] && [[ $(echo ${wheel_members[@]} | grep $user) ]] ; then",
                " empty_passwords=\"1\"",
                " echo -e \"Found the privileged user: $user with an empty password!\"",
                " password=$(tr -dc 'A-Za-z0-9!?%=' < /dev/urandom | head -c 15)",
                " echo -e \"Setting a new password...\"",
                " sudo usermod --password $(echo $password | openssl passwd -1 -stdin) $user",
                "\t\techo -e \"Sending password to AWS Secrets Manager...\"",
                "\t\tepoch_time=$(date +%s)",
                "\t\taws secretsmanager create-secret --name $user\"_password_\"$epoch_time --description \"Account password created automatically via empty password script.\" --secret-string \"$password\" --region us-east-1",
                "\t\taws ssm create-ops-item --title \"Privileged User With Empty Password\" --description \"The privileged user: '$user' was found with an empty password. A complex password was automatically set and stored in Secrets Manager.\" --source ec2 --severity 1 --region us-east-1",
                " fi",
                "",
                "done",
                "",
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

    commandId = response["Command"]["CommandId"]
    response = client.list_command_invocations(CommandId = commandId)
    n = 1
    while(len(response["CommandInvocations"]) == 0 or 0 != len([True for ci in response["CommandInvocations"] if ci["Status"] in ["Pending", "InProgress"] ])):
        response = client.list_command_invocations(CommandId = commandId)
        time.sleep(n)
        n = n * 2
    #print(json.dumps(response, indent = 2, default=str))

    response = client.get_command_invocation(CommandId = commandId, InstanceId = instanceId)
    #print(json.dumps(response, indent = 2, default=str))
    return response

def lambda_handler(event, context):
    if context is None:
        context = {}
    ssm = context.get('ssm')
    if ssm is None:
        print("client not supplied, creating client")
        ssm = boto3.client('ssm')

    if event is None:
        event = {}

    instanceId = event.get("instanceId")
    return remediate(instanceId, ssm)


def build_context():
    global session
    session = boto3.Session(profile_name='nyu')
    return {"ec2": session.client('ec2'), "ssm": session.client("ssm")}

if __name__ == "__main__":
    result = lambda_handler(None, build_context()) 
    print(json.dumps(result, indent = 2))
