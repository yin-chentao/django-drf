# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:16
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("students", views.StudentModelViewSet, basename="students"),
urlpatterns = [] + router.urls
