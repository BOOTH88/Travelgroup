import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from foods.models import Food


def food(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        json_str = request.body
        print('json_str', json_str)
        if not json_str:
            result = {'code': 701, 'error': 'please give me json'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        title = json_obj.get('title')
        if not title:
            result = {'code': 702, 'error': 'please give me title'}
            return JsonResponse(result)
        content = json_obj.get('content')
        if not content:
            result = {'code': 703, 'error': 'please give me content'}
            return JsonResponse(result)
        content_text = json_obj.get('content_text')
        if not content_text:
            result = {'code': 704, 'error': 'please give me content_text'}
            return JsonResponse(result)
        info = content_text[:30]
        location = json_obj.get('location')
        if not location:
            result = {'code': 705, 'error': 'please give me location'}
            return JsonResponse(result)
        Food.objects.create(
            username=request.user,
            title=title,
            content=content,
            info=info,
            location=location
        )
        print('request.user', request.user)
        result = {'code': 200, 'username': request.user.username}
        return JsonResponse(result)
    elif request.method == 'PUT':
        json_str = request.body
        print('json_str', json_str)
        if not json_str:
            result = {'code': 706, 'error': 'please give me json'}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        print('json_obj',json_obj)
        if 'title' not in json_obj:
            json_str = request.body
            print('json_str', json_str)
            if 'title' not in json_str:
                result = {'code': 707, 'error': 'no title'}
                return JsonResponse(result)
            if 'content' not in json_obj:
                result = {'code': 708, 'error': 'no content'}
                return JsonResponse(result)
            if 'info' not in json_obj:
                result = {'code': 709, 'error': 'no info'}
                return JsonResponse(result)
            if 'location' not in json_obj:
                result = {'code': 710, 'error': 'no location'}
                return JsonResponse(result)
            user = request.user
            title = json_obj.get('title','')
            content = json_obj.get('content','')
            info = json_obj.get('info','')
            location = json_obj.get('location','')
            request.user.title = title
            request.user.content = content
            request.user.info = info
            request.user.location = location
            request.user.save()
            result = {'code':200,'username':request.user.username}
            return JsonResponse(result)


            

    elif request.method == 'DELETE':
        pass
    return JsonResponse({'code': 200, 'error': '这是美食'})
