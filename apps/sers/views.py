import json

from django.views import View
from django.http import JsonResponse

from .serializers import Students1Serializer
from apps.student.models import *


# Create your views here.

class StudentView(View):
    def post(self, request):
        # 获取请求数据
        data = json.loads(request.body)
        # 判断是否存在id,不存在则创建,存在则更新
        if data["id"] is None:
            # 反序列化数据
            serializer = Students1Serializer(data=data)
            # 判断数据是否符合要求;不符合则raise_exception=True抛出异常
            serializer.is_valid(raise_exception=True)
            # 序列化只有data参数则save()调用create方法
            serializer.save()
            return JsonResponse({"data": serializer.data, "msg": "保存成功", }, status=201,
                                json_dumps_params={'ensure_ascii': False})
        else:
            try:
                student = Student.objects.get(id=data['id'])
            except Student.DoesNotExist:
                return JsonResponse({"errors": "无数据!"}, status=400, json_dumps_params={'ensure_ascii': False})
            # partial:可以只接受有的参数跳过校验
            serializer = Students1Serializer(instance=student, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            # 序列化存在instance也data参数则save()调用update方法更新数据
            serializer.save()
            return JsonResponse({"data": serializer.data, "msg": "更新成功", }, status=201,
                                json_dumps_params={'ensure_ascii': False})

    def get(self, request):
        students = Student.objects.all()
        serializer = Students1Serializer(students, many=True)
        data = serializer.data

        # data = serializer.data
        return JsonResponse(data=data, safe=False, status=200)
