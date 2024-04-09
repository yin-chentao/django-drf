# -*- coding: utf-8 -*-
# @Time    : 2024/4/8 15:18
# @Author  : yinchentao
# @File    : check_login_middleware.py
import re
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

IGNORE_URL = [
    "/demo/login/"
]



class CheckLoginMiddleware(MiddlewareMixin):
    # 继承MiddlewareMixin类,反射执行process_request,视图返回后执行
    @staticmethod
    def process_request(request):
        """
        该函数在每个函数之前检查是否登录，若未登录，则重定向到/login/
        """
        # 如果请求的路径在跳过列表中，修改标志以跳过JWT校验
        if request.path not in IGNORE_URL and not request.user.is_authenticated:
            # 以下是不用跳转到login页面的url白名单
            return JsonResponse({"msg": "no login"})