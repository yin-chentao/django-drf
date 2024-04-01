from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class StudentAPIView(APIView):

    def get(self, request):
        print(request)  # rest_framework中的request
        print(request._request)  # WSGI中的request
        return Response({'msg': 'ok'})

    def post(self, request):
        print(request.data)
        return Response({'msg': 'ok','code':status.HTTP_200_OK}, status=status.HTTP_200_OK)
