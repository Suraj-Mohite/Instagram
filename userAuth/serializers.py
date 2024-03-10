from rest_framework import serializers
from .models import *
from post.serializers import PostSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username', required=True)
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'location', 'bio', 'url', 'profile_picture']

    def update(self, instance, validated_data):
        profile = instance
        profile.first_name = validated_data.get('first_name', profile.first_name)
        profile.last_name = validated_data.get('last_name', profile.last_name)
        profile.location = validated_data.get('location', profile.location)
        profile.bio = validated_data.get('bio', profile.bio)
        profile.url = validated_data.get('url', profile.url)
        profile.profile_picture = validated_data.get('profile_picture', profile.profile_picture)
        profile.save()
        return profile
