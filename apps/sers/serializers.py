# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:22
# @Author  : yinchentao
# @File    : serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.student.models import *




class Students1Serializer(serializers.ModelSerializer):
    """学生信息序列化器"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=30, min_length=0,
                                 error_messages={"required": "名字不能为空", "max_length": "不能超过30位字符"})
    sex = serializers.IntegerField(required=True, error_messages={"required": "性别不能为空"})
    age = serializers.IntegerField(default=500, max_value=70000, min_value=0,
                                   error_messages={"min_value": "年龄不能小于或等于0"})
    description = serializers.CharField(allow_null=True, allow_blank=True)

    # def create(self, validated_data):
    #     students = Student.objects.create(**validated_data)
    #     return students

    def validate_name(self, data):
        if data in ['django', '菩提老祖']:
            raise serializers.ValidationError(detail='姓名不能为django或菩提老祖', code='validate_name')
        return data


class StudentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {
                "required": True,
                "max_length": 30,
                'error_messages': {
                    "required": "名字不能为空",
                    "max_length": "不能超过30位字符"
                                   }
            },
            'sex': {
                "required": True,
                'error_messages': {
                    "required": "性别不能为空"
                }
                }
        }

    def validate_age(self, value):
        if value <= 0:
            raise ValidationError("年龄不能小于或等于0")
        return value
