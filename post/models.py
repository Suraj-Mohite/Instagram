from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
from .utils import *
import uuid

# Create your models here.

class BaseModel(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse("tags", args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)


class Post(BaseModel):
    caption = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    like = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])
    
    def __str__(self):
        return f"{self.user.username}'s Post on Date: {self.created_at.date()}"
    

class PostImage(models.Model):
    image = models.ImageField(upload_to=get_user_directory_path, null=True, verbose_name="Picture")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.post.user.username}'s post - {self.post.id}"

class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower") #follower
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") #to whome he is following

    def __str__(self):
        return f"{self.follower.username} - {self.following.username}"


class Stream(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="stream_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_user")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_following")
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user

        followers = Follow.objects.filter(following=user)

        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.created_at, following=user)
            stream.save()

    def __str__(self):
        return f"{self.post.user.username} - {self.user.username}"
     
    class Meta:
        ordering = ['-date']


post_save.connect(Stream.add_post, sender=Post)

