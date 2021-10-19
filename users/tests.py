import json
from unittest.mock import MagicMock, patch

from django.test import TestCase, Client

from .models import User


class SignUpTest(TestCase):
    def test_signup_success(self):
        client = Client()
        user = {
            "name": "Mark 1",
            "email": "Mark1@stark.com",
            "password": "mark486**",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Message": "SUCCESS_CREATE"})

    def test_signupview_post_invalid_email_format(self):
        client = Client()
        user = {
            "name": "Mark 1",
            "email": "Mark1starkcom",
            "password": "mark486**",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "INVALID_EMAIL_FORMAT"})

    def test_signupview_post_invalid_password_format(self):
        client = Client()
        user = {
            "name": "Mark 1",
            "email": "Mark1@stark.com",
            "password": "mark486",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "INVALID_PASSWORD_FORMAT"})

    def test_signupview_post_invalid_keys(self):
        client = Client()
        user = {
            "email": "Mark1@stark.com",
            "password": "mark486**",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "KEY_ERROR"})

    def setUp(self):
        User.objects.create(
            name="Mark 2",
            email="Mark2@stark.com",
            password="mark486**",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_duplicated_user(self):
        client = Client()
        user = {
            "name": "Mark 2",
            "email": "Mark2@stark.com",
            "password": "mark486**",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "USER_ALREADY_EXISTS"})


class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            name="Mark 1",
            email="Mark1@stark.com",
            password="$2b$12$XwtwesAaItrhXqS95DtjRuLcz/MxzWluKXrrWkezkiP.eTnZvGhI2",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signinview_post_success(self):
        client = Client()
        user = {
            "email": "Mark1@stark.com",
            "password": "test1234**",
        }

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_signinview_post_unregistered_user(self):
        client = Client()
        user = {
            "email": "Mark123456@stark.com",
            "password": "test1234**",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"Message": "USER_DOES_NOT_EXIST"})

    def test_signinview_post_invalid_password(self):
        client = Client()
        user = {
            "email": "Mark1@stark.com",
            "password": "testtest11223344***",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "INVALID_PASSWORD"})

    def test_signinview_post_invalid_keys(self):
        client = Client()
        user = {
            "email": "Mark1@stark.com",
            "pass": "test1234**",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "KEY_ERROR"})
