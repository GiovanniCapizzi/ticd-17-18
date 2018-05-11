# coding=utf-8
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_index),
    path('list', views.get_algorithms),
    path('<algorithm>', views.algorithm_execute)
]
