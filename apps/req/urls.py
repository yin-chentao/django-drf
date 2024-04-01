# -*- coding: utf-8 -*-
# @Time    : 2024/4/1 17:14
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentAPIView.as_view())
]
