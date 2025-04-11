from django.contrib import admin
from django.urls import path
from apps.my_messages.views import ConversationList, ExcelUploadAPI

urlpatterns = [
    path('api/conversations/', ConversationList.as_view()),
    path('api/upload-excel/', ExcelUploadAPI.as_view(), name='excel-upload'),

]
