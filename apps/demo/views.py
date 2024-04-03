from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookInfoModuleSerializers
from .models import BookInfo


# Create your views here.

class BookInfoAPIView(APIView):
    serializer_book = BookInfoModuleSerializers
    queryset_book = BookInfo.objects.all()

    def get(self, request):
        book_id = request.query_params.get('id', None)
        # 传参存在ID则查询单条数据不存在则查询所有数据
        if book_id:
            try:
                queryset = self.queryset_book.get(id=book_id)
            except BookInfo.DoesNotExist:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "单个无数据!"})
            data_ser = self.serializer_book(queryset)
            res = {'code': status.HTTP_200_OK, 'data': data_ser.data}
            return Response(res)
        else:
            queryset = self.queryset_book
            data_ser = self.serializer_book(queryset, many=True)
            if queryset:
                res = {'code': status.HTTP_200_OK, 'data': data_ser.data}
                return Response(res)
            else:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "无数据!", })

    def post(self, request):
        book_id = request.data.get('id', None)
        data = request.data
        # 传参存在ID则更新数据不存在则新增数据
        if book_id:
            try:
                queryset = self.queryset_book.get(id=book_id)
            except BookInfo.DoesNotExist:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "无数据!"})
            data_ser = self.serializer_book(queryset, data)
            data_ser.is_valid(raise_exception=True)
            data_ser.save()
            res = {'code': status.HTTP_200_OK, "msg": "更新成功", 'data': data_ser.data}
            return Response(res)

        else:
            data_ser = self.serializer_book(data=data)
            data_ser.is_valid(raise_exception=True)
            data_ser.save()
            res = {'code': status.HTTP_200_OK, "msg": "创建成功", 'data': data_ser.data}
            return Response(res)


class BookInfoGenericAPIView(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoModuleSerializers

    def get(self, request):
        book_id = request.query_params.get('id', None)
        # 传参存在ID则查询单条数据不存在则查询所有数据
        if book_id:
            try:
                queryset = self.get_queryset().get(id=book_id)
            except BookInfo.DoesNotExist:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "单个无数据!"})
            data_ser = self.get_serializer(queryset)
            res = {'code': status.HTTP_200_OK, 'data': data_ser.data}
            return Response(res)
        else:
            queryset = self.get_queryset().all()
            data_ser = self.get_serializer(queryset, many=True)
            if queryset:
                res = {'code': status.HTTP_200_OK, 'data': data_ser.data}
                return Response(res)
            else:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "无数据!", })

    def post(self, request):
        book_id = request.data.get('id', None)
        data = request.data
        # 传参存在ID则更新数据不存在则新增数据
        if book_id:
            try:
                queryset = self.get_queryset().get(id=book_id)
            except BookInfo.DoesNotExist:
                return Response({'code': status.HTTP_400_BAD_REQUEST, "msg": "无数据!"})
            data_ser = self.get_serializer(queryset, data)
            data_ser.is_valid(raise_exception=True)
            data_ser.save()
            res = {'code': status.HTTP_200_OK, "msg": "更新成功", 'data': data_ser.data}
            return Response(res)

        else:
            data_ser = self.get_serializer(data=data)
            data_ser.is_valid(raise_exception=True)
            data_ser.save()
            res = {'code': status.HTTP_200_OK, "msg": "创建成功", 'data': data_ser.data}
            return Response(res)
