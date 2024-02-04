from django.urls import path
from .views import IndexAPI, CreatePostAPI

urlpatterns = [
    path("", IndexAPI, name='index'),
    path("create-post/", CreatePostAPI, name='create-post'),
]