from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse

# Data to be served
data = {
  "users": {
    "arn:aws:iam::891376921848:user/group/18/final/user-1-23042024-032248": "user-1-23042024-032248",
    "arn:aws:iam::891376921848:user/group/18/final/user-2-23042024-032248": "user-2-23042024-032248",
    "arn:aws:iam::891376921848:user/group/18/final/user-3-23042024-032248": "user-3-23042024-032248",
    "arn:aws:iam::891376921848:user/group/18/final/user-4-23042024-032248": "user-4-23042024-032248",
    "arn:aws:iam::891376921848:user/group/18/final/user-5-23042024-032248": "user-5-23042024-032248",
    "arn:aws:iam::891376921848:user/group/18/final/user-admin-23042024-032248": "user-admin-23042024-032248"
  },
  "findings": [
    {
      "name": "nyu_ctl_mfa_missing",
      "items": [
        {
          "Arn": "arn:aws:iam::891376921848:user/group/18/final/user-2-23042024-032248",
          "UserName": "user-2-23042024-032248"
        },
        {
          "Arn": "arn:aws:iam::891376921848:user/group/18/final/user-4-23042024-032248",
          "UserName": "user-4-23042024-032248"
        }
      ],
      "description": "Users with console access must have MFA enabled"
    },
    {
      "name": "nyu_ctl_multiple_active_keys",
      "items": [
        {
          "Arn": "arn:aws:iam::891376921848:user/group/18/final/user-1-23042024-032248",
          "UserName": "user-1-23042024-032248"
        },
        {
          "Arn": "arn:aws:iam::891376921848:user/group/18/final/user-3-23042024-032248",
          "UserName": "user-3-23042024-032248"
        }
      ],
      "description": "Multiple Active Access Keys increase surface risk"
    },
    {
      "name": "nyu_ctl_user_with_administrator_access",
      "items": [
        {
          "Arn": "arn:aws:iam::891376921848:user/group/18/final/user-admin-23042024-032248",
          "UserName": "user-admin-23042024-032248"
        }
      ],
      "description": "Users with adminsitrative access increase surface risk"
    }
  ]
}



def index(request):
    return render(request, 'myapp/index.html')

def get_data(request):
    return JsonResponse(data, safe=False)
