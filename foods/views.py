import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from foods.models import Food
from tools.login_check import get_user_by_request, login_check
from user.models import UserProfile


@login_check('POST', 'DELETE')
def food(request, foodie_id=None):
    if request.method == 'GET':
        foodies = UserProfile.objects.filter(
            username=foodie_id
        )
        print('foodie',foodies)
        if not foodies:
            result = {'code': 714, 'error': 'no foodie'}
            return JsonResponse(result)
        # 取出结果中的美食家组
        foodie = foodies[0]
        visitor = get_user_by_request(request)
        visitor_name = None
        # f_location = request.GET.get('location')
        # if f_location:
        #     try:
        #         foodie_food = Food.objects.get(location=f_location)
        #     except Exception as e:
        #         result = {'code': 715, 'error': 'no food'}
        #         return JsonResponse(result)
        #     res = make_foods_res(foodie, f_location)
        #     return JsonResponse(res)
        # if foodie_id:
        #     try:
        #         foodie_food = Food.objects.get(username = foodie_id)
        #     except Exception as e:
        #         result = {'code': 715, 'error': 'no food'}
        #         return JsonResponse(result)
        #     result = {
        #         'code': 200,
        #         'f_id': foodie_id,
        #         'data': {
        #             'title': foodie_food.title,
        #             'image': str(foodie_food.image),
        #             'info': foodie_food.info,
        #             'location': foodie_food.location,
        #             'content': foodie_food.content}
        #     }
        #     return JsonResponse(result)
        if visitor:
            visitor_name = visitor.username

        t_id = request.GET.get('t_id')
        if t_id:
            # 是否自己访问自己
            is_self = False
            # 根据t_id
            t_id = int(t_id)
            if foodie_id == visitor_name:
                is_self = True
                # 美食家访问自己的美食
                try:
                    foodie_food = Food.objects.get(id=t_id)
                except Exception as e:
                    result = {'code': 312, 'error': 'no food'}
                    return JsonResponse(result)
            else:
                # 访客访问美食家的美食
                try:
                    foodie_food = Food.objects.get(id=t_id, limit='public')
                except Exception as e:
                    result = {'code': 313, 'error': 'no food!'}
                    return JsonResponse(result)
            res = make_food_res(foodie, foodie_food, is_self)
            return JsonResponse(res)
        else:
            # /v1/topics/<author_id> 用户全量数据
            # 美食主人 与 user对比
            if foodie_id == visitor_name:

                topics = Food.objects.filter(
                    foodie_id=foodie_id,
                )
            else:
                # 访客 来了,非本人
                topics = Food.objects.filter(
                    foodie_id=foodie_id,
                )
            res = make_foods_res(foodie, topics)
            return JsonResponse(res)
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


def make_foods_res(foodie, foodie_food):
    res = {'code': 200, 'data': {}}
    foods_res = []
    for food in foodie_food:
        d = {}
        d['id'] = food.id
        d['title'] = food.title
        d['image'] = str(food.image)
        d['info'] = food.info
        # TODO content?
        foods_res.append(d)

    res['data']['nickname'] = foodie.nickname
    res['data']['foods'] = foods_res
    # {'code':200, 'data':{'nickname':xxx,'topics':[{xxx},{xx}]}}
    return res


def make_food_res(foodie, foodie_topic, is_self):
    if is_self:
        # 先判断 两者关系
        # 博主访问自己美食
        # 下一篇文章,取出ID大于当前博客ID的第一个,且foodie为当前作者的
        next_topic = Food.objects.filter(id__gt=foodie_topic.id, author=foodie).first()
        # 上一篇文章
        last_topic = Food.objects.filter(id__lt=foodie_topic.id, author=foodie).last()
    else:
        # 访客访问美食
        # 下一篇
        next_topic = Food.objects.filter(id__gt=foodie_topic.id,
                                         author=foodie).first()
        # 上一篇
        last_topic = Food.objects.filter(id__lt=foodie_topic.id, author=foodie).last()

    if next_topic:
        next_id = next_topic.id
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None

    if last_topic:
        last_id = last_topic.id
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None

    res = {'code': 200, 'data': {}}
    res['data']['nickname'] = foodie.nickname
    res['data']['title'] = foodie_topic.title
    res['data']['content'] = foodie_topic.content
    res['data']['info'] = foodie_topic.info
    res['data']['foodie'] = foodie.nickname
    res['data']['next_id'] = next_id
    res['data']['next_title'] = next_title
    res['data']['last_id'] = last_id
    res['data']['last_title'] = last_title
    return res
