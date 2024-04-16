import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.http import HttpResponse, FileResponse
from django.utils.encoding import escape_uri_path

from .customresponse import CustomResponse
from DRF.settings import BASE_DIR
from .serializers import BookInfoModuleSerializers, UploadedFileSerializer
from .models import BookInfo, BookFile
from .mypage import MyPage


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


class BookInfoGenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    # lookup_field = 'pk'
    pagination_class = MyPage
    queryset = BookInfo.objects.all().order_by('id')
    serializer_class = BookInfoModuleSerializers

    def create(self, request, *args, **kwargs):
        # 获取请求的数据列表
        data_list = request.data if isinstance(request.data, list) else [request.data]

        # 对每条数据进行序列化和保存
        serializer = self.get_serializer(data=data_list, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=201, headers=headers)

    def perform_bulk_create(self, serializer):
        serializer.save(createby=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(editby=self.request.user.username)

    def get(self, request, *args, **kwargs):
        # 传参存在ID则查询单条数据不存在则查询所有数据
        if kwargs.get('pk', None):
            return CustomResponse(code=status.HTTP_200_OK, msg='OK', data=[self.retrieve(request).data])
        else:
            return self.list(request)

    def post(self, request, *args, **kwargs):
        # 传参存在ID则更新数据不存在则新增数据
        if kwargs.get('pk', None):
            self.update(request)
            return CustomResponse(code=status.HTTP_200_OK, msg='OK')

        else:
            self.create(request)
            return CustomResponse(code=status.HTTP_200_OK, msg='OK')


class BookInfoDelete(GenericAPIView, DestroyModelMixin):
    serializer_class = BookInfoModuleSerializers
    queryset = BookInfo.objects.all()

    def post(self, request, *args, **kwargs):
        self.destroy(request)
        return Response({'code': status.HTTP_200_OK, "msg": "删除成功", })


class BookFileView(ListCreateAPIView, RetrieveModelMixin, UpdateModelMixin):
    queryset = BookFile.objects.all().order_by('id')
    pagination_class = MyPage
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FileUploadParser)

    def perform_create(self, serializer):
        serializer.save(createby=self.request.user.username)

    def perform_update(self, serializer):
        serializer.save(editby=self.request.user.username)

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            self.update(request)
            return CustomResponse(code=status.HTTP_200_OK, msg='OK')
        else:
            self.create(request)
            return CustomResponse(code=status.HTTP_200_OK, msg='OK')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request)
        else:
            return self.list(request)


class BookFileDownload(GenericAPIView):
    queryset = BookFile.objects.all()
    serializer_class = UploadedFileSerializer
    # parser_classes = (MultiPartParser, FileUploadParser)

    def get(self, request, *args, **kwargs):
        # file_path = request.query_params.get('filename')
        file_name = kwargs.get('filename')
        # file_id = kwargs.get('pk')
        # file_path = str(self.get_queryset().get(id=file_id).file)
        # file_name = str(self.get_queryset().get(id=file_id).file)
        file_path = os.path.join(os.path.join(BASE_DIR, 'media/book'), file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(escape_uri_path(file_name))
            return response
        else:
            return CustomResponse(code=status.HTTP_404_NOT_FOUND, msg="Sorry, the file you requested does not exist.")
