from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        'api/v1/dataextention/info',
        views.get_dataextention_info,
        name='fnc-d'),
    path(
        'api/v1/queryactivity/info',
        views.get_queryactivity_info,
        name='fnc-q'),
    path(
        'api/v1/folderlocation/info',
        views.get_folderlocation_info,
        name='fnc-f'),
]