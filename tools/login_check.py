import jwt
from django.http import JsonResponse

from user.models import UserProfile

key = '1234567'


def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            # 通过request检查token
            # 校验不通过 ,return JsonResponse()
            # user查询出来
            token = request.META.get("HTTP_AUTHORIZATION")
            print(token)
            if request.method not in methods:
                return func(request, *args, **kwargs)
            if not token:
                result = {'code': 107, 'error': 'Please give me token'}
                return JsonResponse(result)
            try:
                res = jwt.decode(token, key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # token过期了
                result = {'code': 108, 'error': 'Please login'}
                return JsonResponse(result)
            except Exception as e:
                result = {'code': 109, 'error': 'Please login'}
                return JsonResponse(result)
            print('res',res)
            username = res['username']
            try:
                user = UserProfile.objects.get(
                    username=username
                )
            except:
                user = None
            if not user:
                result = {'code':110,'error':'no user'}
                return JsonResponse(result)
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return _login_check



def get_user_by_request(request):
    """
    通过request 尝试获取user
    :param request:
    :return:UserProfile o r None
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token,key)
    except:
        return None
    username = res['username']
    try:
        user = UserProfile.objects.get(username=username)
    except:
        return None
    return user
