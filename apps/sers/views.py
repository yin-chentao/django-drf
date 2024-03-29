import json

from django.views import View
from django.http import JsonResponse

from .serializers import Students1Serializer
from apps.student.models import *


# Create your views here.

class StudentView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        serializer = Students1Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({"data": serializer.validated_data, "msg": "保存成功", }, status=200,
                            json_dumps_params={'ensure_ascii': False})

    def get(self, request):
        students = Student.objects.all()
        serializer = Students1Serializer(students, many=True)
        data = serializer.data

        # data = serializer.data
        return JsonResponse(data=data, safe=False, status=200)
