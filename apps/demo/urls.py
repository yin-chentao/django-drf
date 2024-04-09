# -*- coding: utf-8 -*-
# @Time    : 2024/4/1 17:14
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('book/', views.BookInfoAPIView.as_view()),
    path('book1/', views.BookInfoGenericAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    # path('book/<int:pk>', views.BookInfoAPIView.as_view())
]
