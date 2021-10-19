import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from users.decorator import login_decorator
from .models import Post
from users.models import User


class PostsView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            post = data["post"]
            author = request.user

            Post.objects.create(
                post=post,
                author=author,
            )

            return JsonResponse({"Message": "SUCCESS_CREATE"}, status=201)

        except KeyError:
            return JsonResponse({"Message": "KEY_ERROR"}, status=400)

    def get(self, request):
        OFFSET = int(request.GET.get("offset", "0"))
        LIMIT = int(request.GET.get("limit", "10"))
        POSTING_COUNT = Post.objects.all().count()

        if POSTING_COUNT < LIMIT:
            LIMIT = POSTING_COUNT

        posts = (
            Post.objects.all().select_related("author").order_by("-id")[OFFSET:LIMIT]
        )

        data = [
            {
                "post": post.post,
                "author": post.author.name,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for post in posts
        ]

        result = {
            "count": len(posts),
            "data": data,
        }

        return JsonResponse({"Result": result}, status=200)


class PostView(View):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            result = {
                "post": post.post,
                "author": post.author.name,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }

            return JsonResponse({"Result": result}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({"Message": "POST_DOES_NOT_EXIST"}, status=404)

    @login_decorator
    def patch(self, request, post_id):
        try:
            data = json.loads(request.body)
            post_obj = Post.objects.get(id=post_id)

            if post_obj.author != request.user:
                return JsonResponse({"Message": "NOT_AUTHORIZATION_USER"}, status=403)

            post_obj.post = data["post"]
            post_obj.save()

            return JsonResponse({"Message": "SUCESS_UPDATE"}, status=201)

        except KeyError:
            return JsonResponse({"Message": "KEY_ERROR"}, status=400)

        except Post.DoesNotExist:
            return JsonResponse({"Message": "POST_DOES_NOT_EXIST"}, status=404)

    @login_decorator
    def delete(self, request, post_id):
        try:
            post_obj = Post.objects.get(id=post_id)

            if post_obj.author != request.user:
                return JsonResponse({"Message": "NOT_AUTHORIZATION_USER"}, status=403)

            post_obj.delete()

            return HttpResponse(status=204)

        except Post.DoesNotExist:
            return JsonResponse({"Message": "POST_DOES_NOT_EXIST"}, status=404)
