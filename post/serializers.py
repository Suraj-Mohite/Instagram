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

class LikesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Likes
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True)
    post_images = PostImageSerializer(many=True, read_only=True) #post_images is related name in models
    absolute_url = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, #file size in bytes
            allow_empty_file=False, #empty file not allowed
            use_url=False), #This attribute determines whether to use the file URL when serializing the image. When use_url is set to False, the actual file data will be included in the serialized output instead of a URL
        write_only=True,
        required=False
    )
    class Meta:
        model = Post
        # fields = ["id", "tags", "post_images", "created_at", "updated_at", "uploaded_images", "user"]
        fields = '__all__'

    def create(self, validated_data):
        captions = validated_data.get('caption', None)
        images_data = validated_data.pop('uploaded_images', [])
        post = super().create(validated_data)
        if captions:
            tag_list = get_tag_list_from_caption(captions)
            for word in tag_list:
                tag_obj, created = Tag.objects.get_or_create(title=word)
                post.tags.add(tag_obj)

        if not images_data:
            raise serializers.ValidationError("uploaded_images field required")
        for image_data in images_data:
            PostImage.objects.create(post=post, image=image_data)

        return post
    
    def update(self, instance, validated_data):
        captions = validated_data.get('caption', None)
        uploaded_images = validated_data.get('uploaded_images', None)

        if uploaded_images:
            raise serializers.ValidationError("Can not change images once upload during post creation.")
        
        post = instance
        post.caption = captions
        if captions:
            tag_list = get_tag_list_from_caption(captions)
            new_tag_obj_list = []
            for word in tag_list:
                tag_obj, created = Tag.objects.get_or_create(title=word)
                new_tag_obj_list.append(tag_obj)
            
            post.tags.set(new_tag_obj_list)
        else:
            raise serializers.ValidationError("Invalid request")
        
        post.save()
        return post
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = "__all__"

class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = '__all__'