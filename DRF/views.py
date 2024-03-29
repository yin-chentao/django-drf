import json

from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def home(request):
    response = {"主页": "hello world"}
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
