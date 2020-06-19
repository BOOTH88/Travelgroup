import hashlib
import json
import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from user.models import UserProfile


def tokens(request):
    # 前端的地址是:127.0.0.1:5000/login
    # 获取前端传递过来的数据/生成token
    # 获取-校验密码-生成token
    if not request.method =='POST':
        result = {'code':101,'error':'Please use POST method'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code':102,'error':'please give me json'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    password = json_obj.get('password')
    if not username:
        result = {'code':103,'error':'please give me username'}
        return JsonResponse(result)
    if not password:
        result = {'code':104,'error':'please give me username'}
        return JsonResponse(result)
    # 如果用户名及密码都为值

    user = UserProfile.objects.filter(username=username)
    if not user:
        result = {'code':105,'error':'username or password is wrong!!'}
        return JsonResponse(result)
    user = user[0]
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code':106,'error':'username or password is wrong!'}
        return JsonResponse(result)

    # 生成token
    token = make_token(username)
    result =  {'code':200,'username':username,
               'data':{'token':token.decode()}}
    return JsonResponse(result)

def make_token(username, exprie=24 * 3600):
    key = '1234567'
    now = time.time()
    payload = {'username': username, 'exp': int(now + exprie)}
    return jwt.encode(payload, key, algorithm='HS256')
