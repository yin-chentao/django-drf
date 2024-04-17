# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 14:42
# @Author  : yinchentao
# @File    : serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BookInfo, BookFile


class BookInfoModuleSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ["id", "name", "author", "lend", "description"]
        read_only_fields = ["id", "createby", "editby"]
        extra_kwargs = {"name": {"required": True, "max_length": 30,
                                 "error_messages": {"required": "缺少书籍名字", "max_length": "不能超过30位字符",
                                                    "blank": "书籍名字不能为空"}}}


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        fields = '__all__'
        read_only_fields = ["id", "createby", "editby"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        read_only_fields = ['id']
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserPasswordChange(serializers.ModelSerializer):
    new_password = serializers.CharField()
    password_confirmation = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'new_password', 'password_confirmation']
        read_only_fields = ['id']
        extra_kwargs = {"password": {"write_only": True}, "new_password": {"write_only": True},
                        "password_confirmation": {"write_only": True}, "id": {"read_only": True}}
