import jwt

from django.http import JsonResponse

from config.settings import SECRET_KEY
from users.models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.META["HTTP_AUTHORIZATION"]
            payload = jwt.decode(access_token, SECRET_KEY, algorithms="HS256")
            request.user = User.objects.get(id=payload["id"])

        except jwt.exceptions.DecodeError:
            return JsonResponse({"Message": "INVALID_TOKEN"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"Message": "INVALID_USER"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper
