import json, jwt
from datetime import datetime, timedelta

from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client

from .models import Post
from users.models import User
from config.settings import SECRET_KEY


class ContentTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            name="Mark",
            email="Mark1@stark.com",
            password="mark486**",
        )

        User.objects.create(
            id=2,
            name="Shin",
            email="Shin1@stark.com",
            password="shin486**",
        )

        Post.objects.create(
            id=1,
            post="i'm wecoder1",
            author=User.objects.get(id=1),
        )

        Post.objects.create(
            id=2,
            post="i'm wecoder2",
            author=User.objects.get(id=1),
        )

        Post.objects.create(
            id=3,
            post="i'm wecoder3",
            author=User.objects.get(id=1),
        )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_create_post_success(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}

        posting = {
            "post": "i'm wecoder4",
        }
        response = client.post(
            "/posts", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Message": "SUCCESS_CREATE"})

    def test_create_key_error(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}

        posting = {
            "posting": "i'm wecoder4",
        }
        response = client.post(
            "/posts", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "KEY_ERROR"})

    def test_get_getlist_success(self):
        client = Client()
        response = client.get("/posts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "Result": {
                    "count": 3,
                    "data": [
                        {
                            "post": "i'm wecoder3",
                            "author": "Mark",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        },
                        {
                            "post": "i'm wecoder2",
                            "author": "Mark",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        },
                        {
                            "post": "i'm wecoder1",
                            "author": "Mark",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        },
                    ],
                }
            },
        )

    def test_post_get_success(self):
        client = Client()
        response = client.get("/posts/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "Result": {
                    "post": "i'm wecoder1",
                    "author": "Mark",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            },
        )

    def test_post_does_not_exist(self):
        client = Client()
        response = client.get("/posts/10")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Message": "POST_DOES_NOT_EXIST"})

    def test_post_edit_not_authorization_user(self):
        access_token = jwt.encode(
            {
                "id": 2,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        posting = {
            "post": "edit posting i'm wecoder4",
        }
        response = client.patch(
            "/posts/1", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "NOT_AUTHORIZATION_USER"})

    def test_post_edit_success(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        posting = {
            "post": "edit posting i'm wecoder4",
        }
        response = client.patch(
            "/posts/1", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"Message": "SUCESS_UPDATE"})

    def test_post_edit_key_error(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        posting = {
            "posting": "edit posting i'm wecoder4",
        }
        response = client.patch(
            "/posts/1", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"Message": "KEY_ERROR"})

    def test_post_edit_does_not_exist(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        posting = {
            "posting": "edit posting i'm wecoder4",
        }
        response = client.patch(
            "/posts/10", json.dumps(posting), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Message": "POST_DOES_NOT_EXIST"})

    def test_post_delete_not_authorization_user(self):
        access_token = jwt.encode(
            {
                "id": 2,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/1", **header)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"Message": "NOT_AUTHORIZATION_USER"})

    def test_post_delete_success(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/1", **header)

        self.assertEqual(response.status_code, 204)

    def test_post_delete_does_not_exist(self):
        access_token = jwt.encode(
            {
                "id": 1,
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/posts/10", **header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Message": "POST_DOES_NOT_EXIST"})
