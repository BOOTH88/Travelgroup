import hashlib
import json
import time
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from btoken.views import make_token
from tools.login_check import login_check

# Create your views here.
@login_check('PUT')
def users(request, username=None):
    if request.method == 'GET':
        # 获取用户数据
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                user = None
            if not user:
                result = {'code': 208, 'error': 'no user'}
                return JsonResponse(result)
            # 检查是否有查询字符串
            if request.GET.keys():
                # 查询指定的字符串
                data = {}
                for k in request.GET.keys():
                    if hasattr(user, k):
                        v = getattr(user, k)
                        if k == 'avatar':
                            data[k] = str(v)
                        else:
                            data[k] = v
                result = {'code': 200, 'username': username, 'data': data}
                return JsonResponse(result)
            else:
                # 全量查询 (password,email,不给)
                result = {
                    'code': 200,
                    'username': username,
                    'data': {'info': user.info,
                             'sign': user.sign,
                             'avatar': str(user.avatar),
                             'nickname': user.nickname}
                }
                return JsonResponse(result)

            # return JsonResponse({'code':200,'error':'我来了GET  %s'%(username)})
        else:
            return JsonResponse({'code': 200, 'error': '我来了GET'})
    elif request.method == 'POST':
        # request.POST 不能拿到json的内容
        # 创建用户
        print(request.body)
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        username = json_obj.get('username')
        if not username:
            result = {'code': 202, 'error': 'Please give me username'}
            return JsonResponse(result)
        email = json_obj.get('email')
        if not email:
            result = {'code': 203, 'error': 'Please give me email'}
            return JsonResponse(result)
        password_1 = json_obj.get('password_1')
        password_2 = json_obj.get('password_2')
        if not password_1 or not password_2:
            result = {'code': 204, 'error': 'Please give me password'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 205, 'error': 'Please give me password2 same as password1'}
            return JsonResponse(result)

        # 此时,检查当前数据库是否有此用户
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 206, 'error': 'Your username is already existed!'}
            return JsonResponse(result)
        # 处理密码 md5/哈希/散列
        m = hashlib.md5()
        m.update(password_1.encode())
        # 个人签名 /个人信息可以为空
        sign = info = ''
        try:
            UserProfile.objects.create(
                username=username,
                nickname=username,
                password=m.hexdigest(),
                sign=sign,
                info=info,
                email=email,
            )
        except Exception as e:
            result = {'code': 207, 'error': 'Server is busy'}
            return JsonResponse(result)
        # 生成token
        token = make_token(username)
        # 正常返回给前端
        result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
        return JsonResponse(result)
    elif request.method == 'PUT':
        # 用户修改数据
        # http://127.0.0.1:5000/<username>/change_info
        # 此头可获取前端传过来的token
        # META可拿取http协议原生请求头,META也是字典对象,可以使用字典相关的方法
        # 特别注意 http头有可能被django重命名,建议百度
        print('***********************')
        json_str = request.body
        if not json_str:
            resutl = {'code': 209, 'error': 'Please give me json'}
            return JsonResponse(resutl)
        json_obj = json.loads(json_str)
        print('json_obj',json_obj)
        if 'sign' not in json_obj:
            result = {'code': 210, 'error': 'no sign'}
            return JsonResponse(result)
        if 'info' not in json_obj:
            result = {'code': 211, 'error': 'no info'}
            return JsonResponse(result)
        user = request.user
        sign = json_obj.get('sign', '')
        info = json_obj.get('info', '')
        request.user.sign = sign
        request.user.info = info
        request.user.save()
        result = {'code': 200, 'username': request.user.username}
        return JsonResponse(result)

    else:
        raise
    return JsonResponse({'code': 200})


@login_check('POST')
def user_avatar(request,username=None):
    '''
    上传个人头像
    :param request:
    :param username:
    :return:
    '''
    if request.method != "POST":
        result = {'code':212,'error':'我需要post请求,好吗?'}
        return JsonResponse(result)
    #获取用户头像,通过FILES来得到
    avatar = request.FILES.get('avatar')
    if not avatar:
        result = {'code':213,'error':'我需要头像!'}
        return JsonResponse(result)
    # 判断url中的username  是否和token的私有声明的usename是否一样,
    # 如果不一样,则报错
    request.user.avatar = avatar
    request.user.save()
    result = {'code':200,'username':request.user.username}
    return JsonResponse(result)






    return JsonResponse({'code':200,'error':'头像'})