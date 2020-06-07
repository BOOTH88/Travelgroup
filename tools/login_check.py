import jwt
from django.http import JsonResponse

from user.models import UserProfile

key = '54321'


def login_check(*methods):
    def login(func):
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            print(token)
            if request.method not in methods:
                return func(request, *args, **kwargs)
            if not token:
                result = {'code': 101, 'error': 'give me token'}
                return JsonResponse(result)
            try:
                res = jwt.decode(token, key, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                result = {'code': 108, 'error': 'Please login'}
                return JsonResponse(result)
            except Exception as e:
                result = {'code': 109, 'error': 'Please login'}
                return JsonResponse(result)
            print('res', res)
            username = res['username']
            try:
                user = UserProfile(
                    username=username
                )
            except:
                user = None
            if not user:
                result = {'code': 110, 'error': 'no user'}
                return JsonResponse(result)
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return login
