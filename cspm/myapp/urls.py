from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iam/setup/', views.iam_setup, name='iam_setup'),
    path('iam/teardown/', views.iam_teardown, name='iam_teardown'),
    path('iam/scan/', views.iam_scan, name='iam_scan'),
]
