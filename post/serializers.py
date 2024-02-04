from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True)
    post_images = PostImageSerializer(many=True, read_only=True) #post_images is related name in models
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, #file size in bytes
            allow_empty_file=False, #empty file not allowed
            use_url=False), #This attribute determines whether to use the file URL when serializing the image. When use_url is set to False, the actual file data will be included in the serialized output instead of a URL
        write_only=True
    )
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        captions = validated_data.get('caption', None)
        images_data = validated_data.pop('uploaded_images')
        post = super().create(validated_data)
        if captions:
            tag_list = get_tag_list_from_caption(captions)
            for word in tag_list:
                tag_obj, created = Tag.objects.get_or_create(title=word)
                post.tags.add(tag_obj)

        for image_data in images_data:
            PostImage.objects.create(post=post, image=image_data)

        return post

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = "__all__"