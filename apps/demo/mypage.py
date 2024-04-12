# -*- coding: utf-8 -*-
# @Time    : 2024/4/10 17:32
# @Author  : yinchentao
# @File    : mypage.py
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .customresponse import CustomResponse


class MyPage(PageNumberPagination):
    page_size = 3  # 每页显示数量
    max_page_size = 2000  # 每页最大显示数量。
    page_size_query_param = 'size'  # 每页数量的参数名称
    page_query_param = 'page'  # 页码的参数名称

    def get_paginated_response(self, data):
        return CustomResponse(data=data, code=200, msg="OK", status=status.HTTP_200_OK, count=self.page.paginator.count,
                              next=self.get_next_link(), previous=self.get_previous_link())
