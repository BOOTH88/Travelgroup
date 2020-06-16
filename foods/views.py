import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from foods.models import Food
from tools.login_check import get_user_by_request, login_check
from user.models import UserProfile


@login_check('POST', 'DELETE', 'PUT')
def food(request, foodie_id=None):
    if request.method == 'GET':
        foodies = UserProfile.objects.filter(
            username=foodie_id
        )
        if not foodies:
            result = {'code': 714, 'error': 'no foodie'}
            return JsonResponse(result)
        # 取出结果中的美食家组
        foodie = foodies[0]
        # visitor = get_user_by_request(request)
        # visitor_name = None
        f_location = request.GET.get('location')
        if f_location:
            try:
                foodie_food = Food.objects.get(location=f_location)
            except Exception as e:
                result = {'code': 715, 'error': 'no food'}
                return JsonResponse(result)
            res = make_foods_res(foodie, f_location)
            return JsonResponse(res)
        f_id = request.GET.get('f_id')
        if f_id:
            try:
                foodie_food = Food.objects.get(id=f_id)
            except Exception as e:
                result = {'code': 715, 'error': 'no food'}
                return JsonResponse(result)
            result = {
                'code': 200,
                'f_id': f_id,
                'data': {
                    'title': foodie_food.title,
                    'image': str(foodie_food.image),
                    'info': foodie_food.info,
                    'location': foodie_food.location,
                    'content': foodie_food.content}
            }
            return JsonResponse(result)


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
            foodie=request.user,
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
        print('json_obj', json_obj)
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
            title = json_obj.get('title', '')
            content = json_obj.get('content', '')
            info = json_obj.get('info', '')
            location = json_obj.get('location', '')
            request.user.title = title
            request.user.content = content
            request.user.info = info
            request.user.location = location
            request.user.save()
            result = {'code': 200, 'username': request.user.username}
            return JsonResponse(result)




    elif request.method == 'DELETE':
        foodie = request.user
        print(foodie)
        token_foodie_id = foodie.username
        print('foodie_id', foodie_id)
        print('token_foodie_id', token_foodie_id)
        if foodie_id != token_foodie_id:
            result = {'code': 711, 'error': 'you can not do it'}
            return JsonResponse(result)
        food_id = request.GET.get('food_id')
        try:
            food = Food.objects.get(id=food_id)
        except:
            result = {'code': 712, 'error': 'you can not do it'}
            return JsonResponse(result)
        if food.foodie.username != foodie_id:
            result = {'code': 713, 'error': 'you can not do it'}
            return JsonResponse(result)

        food.delete()
        res = {'code': 200}
        return JsonResponse(res)
    return JsonResponse({'code': 200, 'error': '这是美食'})


def make_foods_res(foodie, f_location):
    res = {'code': 200, 'data': {}}
    foods_res = []
    for keyword in f_location:
        d = {}
        d['id'] = keyword.id
        d['title'] = keyword.title
        d['image'] = str(keyword.image)
        d['info'] = keyword.info
        # TODO content?
        foods_res.append(d)

    res['data']['keyword'] = foodie.location
    res['data']['foods'] = foods_res
    # {'code':200, 'data':{'nickname':xxx,'topics':[{xxx},{xx}]}}
    return res
