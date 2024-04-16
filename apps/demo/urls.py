# -*- coding: utf-8 -*-
# @Time    : 2024/4/1 17:14
# @Author  : yinchentao
# @File    : urls.py
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from rest_framework import routers  # 导入路由函数
route = routers.DefaultRouter()  # 创建路由
# route.register('book2', viewset=views.BookInfoModelViewSet)

urlpatterns = [
    path('book/', views.BookInfoAPIView.as_view()),
    path('book1/', views.BookInfoGenericAPIView.as_view()),
    path('book1/<int:pk>/', views.BookInfoGenericAPIView.as_view()),
    path('book1/del/<int:pk>/', views.BookInfoDelete.as_view()),
    path('book1/upload/', views.BookFileView.as_view()),
    path('book1/upload/<int:pk>/', views.BookFileView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    # path('book/<int:pk>', views.BookInfoAPIView.as_view())
] + route.urls  # 将创建的路由添加到列表

