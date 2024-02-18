from django.urls import path
from .views import IndexAPI, CreatePostAPI, PostDetailAPI, LikeAPI, SavePostAPI

urlpatterns = [
    path("", IndexAPI, name='index'),
    path("create-post/", CreatePostAPI, name='create-post'),
    path("post-detail/<uuid:id>", PostDetailAPI, name='post-detail'),
    path("<uuid:id>/like/", LikeAPI, name='post-like'),
    path("<uuid:id>/save-post/", SavePostAPI, name='post-save'),
    # path("<uuid:id>/save-post-new/", SavePostNewAPI, name='post-save-new'),
]