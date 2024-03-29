# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:22
# @Author  : yinchentao
# @File    : serializers.py
from rest_framework import serializers
from .models import Student


class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
