from django.contrib import admin
from django.urls import path
from apps.my_messages.views import ConversationAPI, ExcelUploadAPI

urlpatterns = [
    path('api/conversations/', ConversationAPI.as_view()),
    path('api/upload-excel/', ExcelUploadAPI.as_view(), name='excel-upload'),

]
