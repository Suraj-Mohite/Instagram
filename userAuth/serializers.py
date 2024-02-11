from rest_framework import serializers
from .models import *
from post.serializers import PostSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    favourite = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
