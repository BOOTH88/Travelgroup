import json
import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def tokens(request):
    if not request.nethod == 'POST':
        result = {'code':101,'error':'method is wrong'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code':102,'error':'please give me json'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    password = json_obj.get('password')
    if not username:
        result = {'code': 103, 'error': 'please give me username'}
        return JsonResponse(result)
    if not password:
        result = {'code': 104, 'error': 'please give me password'}
        return JsonResponse(result)




def make_token(username, exprie=24 * 3600):
    key = '1234567'
    now = time.time()
    payload = {'username': username, 'exp': int(now + exprie)}
    return jwt.encode(payload, key, algorithm='HS256')