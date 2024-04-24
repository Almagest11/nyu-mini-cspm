import json
import boto3
import sys

PATH_PREFIX = "/group/18/final/"

global session

def list_users(client) :
    users = client.list_users(PathPrefix = PATH_PREFIX)
    return {user['Arn']: user['UserName'] for user in users['Users']}

def nyu_ctl_mfa_missing(client, users):
    findings = {"name": sys._getframe().f_code.co_name, "items": [], "description": "Users with console access must have MFA enabled"}
    for arn, userName in users.items():
        try:
            client.get_login_profile(UserName = userName)
            result = client.list_mfa_devices(UserName = userName)
            if len(result.get('MFADevices', [])) == 0:
                findings.get('items').append({"Arn": arn, "UserName": userName})
        except:
            pass
    return findings

def nyu_ctl_multiple_active_keys(client, users):
    findings = {"name": sys._getframe().f_code.co_name, "items": [], "description": "Multiple Active Access Keys increase surface risk"}
    for arn, userName in users.items():
        result = client.list_access_keys(UserName = userName)
        if len([ akmd for akmd in result.get('AccessKeyMetadata', []) if akmd['Status'] == 'Active' ]) > 1:
            findings.get('items').append({"Arn": arn, "UserName": userName})
    return findings


def nyu_ctl_user_with_administrator_access(client, users):
    adminPolicyArn = 'arn:aws:iam::aws:policy/AdministratorAccess'
    findings = {"name": sys._getframe().f_code.co_name, "items": [], "description": "Users with adminsitrative access increase surface risk"}
    for arn, userName in users.items():
        result = client.list_attached_user_policies(UserName=userName)['AttachedPolicies']
        if any(policy['PolicyArn'] == adminPolicyArn for policy in result):
            findings.get('items').append({"Arn": arn, "UserName": userName})
    return findings


def lambda_handler(event, context):
    if context is None:
        context = {}
    client = context.get('iam')
    if client is None:
        print("client not supplied, creating client")
        client = boto3.client('iam')

    findings = []
    users = list_users(client)
    findings.append(nyu_ctl_mfa_missing(client, users))
    findings.append(nyu_ctl_multiple_active_keys(client, users))
    findings.append(nyu_ctl_user_with_administrator_access(client, users))

    return {"users":users, "findings": findings}

def build_context():
    global session
    session = boto3.Session(profile_name='nyu')
    return {"iam": session.client('iam')}


if __name__ == "__main__":
    result = lambda_handler(None, build_context()) 
    print(json.dumps(result, indent = 2))