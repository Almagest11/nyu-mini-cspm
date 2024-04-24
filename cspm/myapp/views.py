from django.shortcuts import render
from django.http import JsonResponse

def index(request):
  return render(request, 'myapp/index.html')

def iam_setup(request):
  from .iam.tf.tf import setup
  setup()
  return JsonResponse({}, safe=False)

def iam_teardown(request):
  from .iam.tf.tf import teardown
  teardown()
  return JsonResponse({}, safe=False)

def iam_scan(request):
  from .iam.rules.scan import lambda_handler, build_context
  data = lambda_handler(None, build_context())
  return JsonResponse(data, safe=False)

