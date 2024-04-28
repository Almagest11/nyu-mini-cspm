from django.shortcuts import render
from django.http import JsonResponse

def index(request):
  return render(request, 'myapp/index.html')


def iam_index(request):
  return render(request, 'myapp/iam/index.html')

def ec_index(request):
  return render(request, 'myapp/ec/index.html')

def net_index(request):
  return render(request, 'myapp/net/index.html')

def vem_index(request):
  return render(request, 'myapp/vem/index.html')


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


def ec_setup(request):
  from .ec.tf.tf import setup
  setup()
  return JsonResponse({}, safe=False)

def ec_teardown(request):
  from .ec.tf.tf import teardown
  teardown()
  return JsonResponse({}, safe=False)

def ec_scan(request):
  from .ec.rules.scan import lambda_handler, build_context
  data = lambda_handler(None, build_context())
  return JsonResponse(data, safe=False)

def ec_remediate(request, instanceId):
  from .ec.rules.remediate import lambda_handler, build_context
  data = lambda_handler({"instanceId": instanceId}, build_context())
  return JsonResponse(data, safe=False)

def net_setup(request):
  from .net.tf.tf import setup
  setup()
  return JsonResponse({}, safe=False)

def net_teardown(request):
  from .net.tf.tf import teardown
  teardown()
  return JsonResponse({}, safe=False)

def net_scan(request):
  from .net.rules.scan import lambda_handler, build_context
  data = lambda_handler(None, build_context())
  return JsonResponse(data, safe=False)

