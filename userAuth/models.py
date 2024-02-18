from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from base.models import BaseModel
from base.utils import get_user_directory_path
# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=get_user_directory_path, default="default.jpg")

    def __str__(self):
        return self.user.username