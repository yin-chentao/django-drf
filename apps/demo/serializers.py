# -*- coding: utf-8 -*-
# @Time    : 2024/4/3 14:42
# @Author  : yinchentao
# @File    : serializers.py
from rest_framework import serializers

from .models import BookInfo


class BookInfoModuleSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ["id", "name", "author", "lend", "description"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {
                "required": True,
                "max_length": 30,
                "error_messages": {
                    "required": "缺少书籍名字",
                    "max_length": "不能超过30位字符",
                    "blank": "书籍名字不能为空"
                                   }
            }
        }

