import json

from django.shortcuts import render, redirect
from accredit.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from accredit.util.jwt_auth import encode_auth_token
from django.views.decorators.csrf import csrf_exempt
import time


# Create your views here.
def index(request):
    return render(request, "login/index.html", {})


@method_decorator(csrf_exempt, name="dispatch")
def login(request):
    if request.method == 'POST':
        request_body=json.loads(request.body)
        username = request_body.get('username', '')
        password = request_body.get('password', '')
        user = User.objects
        if user.filter(user_name=username, password=password, status=1).first():
            token = encode_auth_token(username)
            user.filter(user_name=username, password=password, status=1).update(login_time=time.time())
            return JsonResponse({'status': True, 'msg': '', "token": token})
        elif User.objects.filter(user_name=username, password=password, status=0).first():
            return JsonResponse({'status': False, 'msg': '该用户已被锁定'})
        else:
            return JsonResponse({"status": False, 'msg': "用户名密码错误"})

    return render(request, 'login/login.html')


@method_decorator(csrf_exempt, name="dispatch")
def register(request):
    if request.method == 'POST':
        request_body=json.loads(request.body)
        email=request_body.get('email')
        username=request_body.get('username')
        password=request_body.get('password')
        msg = '注册成功'
        if User.objects.filter(email=email).first():
            msg = '邮箱已存在'
            return JsonResponse({'status': False, 'msg': msg})
        if User.objects.filter(user_name=username).first():
            msg = '用户名已存在'
            return JsonResponse({'status': False, 'msg': msg})

        user = User.objects.create(email=email, password=password, user_name=username, token='123')
        User.save(user)
        return JsonResponse({'status': True, 'msg': msg})

    return render(request, 'login/register.html')
