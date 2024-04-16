"""
URL configuration for DRF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from DRF import views
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.demo import views as demo_views
from django.urls import path, include

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('api/', include('apps.student.urls')),
    path('sers/', include('apps.sers.urls')),
    path('req/', include('apps.req.urls')),
    path('demo/', include('apps.demo.urls')),
    path('login/', TokenObtainPairView.as_view()),
    path('media/book/<str:filename>/', demo_views.BookFileDownload.as_view()),

]
