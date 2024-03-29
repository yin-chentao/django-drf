# -*- coding: utf-8 -*-
# @Time    : 2024/3/29 9:54
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('students1/', views.StudentView.as_view())
]
