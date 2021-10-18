import json, re, jwt, bcrypt

from django.views import View
from django.http import JsonResponse
from django.db.utils import DataError

from .models import User
from config.settings import SECRET_KEY


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_format = re.compile("\w+[@]\w+[.]\w+")
        password_format = re.compile(
            "^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$"
        )

        try:
            if not email_format.search(data["email"]):
                return JsonResponse({"Message": "INVALID_EMAIL_FORMAT"}, status=400)
            if not password_format.match(data["password"]):
                return JsonResponse({"Message": "INVALID_PASSWORD_FORMAT"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"Message": "USER_ALREADY_EXISTS"}, status=400)

            salt = bcrypt.gensalt()
            encoded_passwrod = data["password"].encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_passwrod, salt)
            decoded_password = hashed_password.decode("utf-8")

            User.objects.create(
                name=data["name"],
                password=decoded_password,
                email=data["email"],
            )
            return JsonResponse({"Message": "SUCCESS_CREATE"}, status=201)

        except KeyError:
            return JsonResponse({"Message": "KEY_ERROR"}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"Message": "USER_DOES_NOT_EXIST"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"Message": "INVALID_PASSWORD"}, status=403)

            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse(
                {"Message": "LOGIN_SUCCESS", "token": access_token}, status=200
            )

        except KeyError:
            return JsonResponse({"Message": "KEY_ERROR"}, status=400)
