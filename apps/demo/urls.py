# -*- coding: utf-8 -*-
# @Time    : 2024/4/1 17:14
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.BookInfoAPIView.as_view()),
    path('book1/', views.BookInfoGenericAPIView.as_view()),
    # path('book/<int:pk>', views.BookInfoAPIView.as_view())
]
