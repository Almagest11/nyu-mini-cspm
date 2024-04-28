from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iam/', views.iam_index, name='index'),
    path('vem/', views.vem_index, name='index'),
    path('ec/', views.ec_index, name='index'),
    path('net/', views.net_index, name='index'),
    path('iam/setup/', views.iam_setup, name='iam_setup'),
    path('iam/teardown/', views.iam_teardown, name='iam_teardown'),
    path('iam/scan/', views.iam_scan, name='iam_scan'),
    path('ec/setup/', views.ec_setup, name='ec_setup'),
    path('ec/teardown/', views.ec_teardown, name='ec_teardown'),
    path('ec/scan/', views.ec_scan, name='ec_scan'),
    path('ec/remediate/<slug:instanceId>', views.ec_remediate, name='ec_remediate'),
    path('net/setup/', views.net_setup, name='net_setup'),
    path('net/teardown/', views.net_teardown, name='net_teardown'),
    path('net/scan/', views.net_scan, name='net_scan'),
]
