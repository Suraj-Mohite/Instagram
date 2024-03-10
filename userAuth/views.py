from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

from django.urls import resolve
from django.http import Http404
from django.db import transaction
from django.contrib.auth.models import User

from .models import Profile
from post.models import Post, Stream, Follow
from .serializers import ProfileSerializer
from post.serializers import PostSerializer, SavedPostSerializer

import logging
import sys
import json

logger = logging.getLogger(__name__)
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserProfileAPIView(APIView):

    pagination_class = PageNumberPagination

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise Http404(e)
        
    def get(self, request, username, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'
        response['data'] = {}

        try:
            user = self.get_object(username) #other user
            profile_obj = Profile.objects.get(user=user)
            url_name = resolve(request.path).url_name
            if url_name == "user-posts":
                posts = Post.objects.filter(user=user).order_by('-created_at')
            elif url_name == "user-saved":
                # User can not see other users saved post
                if user == request.user:
                    posts = Post.objects.filter(post_saved__profile=profile_obj).order_by("-post_saved__created_at") # here post_saved is related name in SavedPost model connected post with it with foreignkey
                else:
                    response['status'] = 403
                    response['message'] = 'You don\'t have permission to view this content.'
                    return Response(response, status=status.HTTP_403_FORBIDDEN)


            #post, followers and following count
            post_count = Post.objects.filter(user=user).count()
            followers_count = Follow.objects.filter(following = user).count()
            following_count = Follow.objects.filter(follower = user).count()

            #follow status
            follow_status = Follow.objects.filter(follower = request.user, following = user).exists()

            #Pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(posts, request)
            post_serializer = PostSerializer(paginated_queryset, many=True)
            profile_serializer = ProfileSerializer(profile_obj)
            # serializer = PostSerializer(posts, many=True)

            response['status'] = 200
            response['message'] = 'Success'
            response['data']['profile'] = profile_serializer.data
            response['data']['profile']['post_count'] = post_count
            response['data']['profile']['followers_count'] = followers_count
            response['data']['profile']['following_count'] = following_count
            response['data']['profile']['follow_status'] = follow_status
            response['data']['posts'] = post_serializer.data

            return Response(response, status=status.HTTP_200_OK)
        
        except NotFound as e:
            response['status'] = 404
            response['message'] = 'Page not found'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("UserProfileAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'userAuth'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

UserProfile = UserProfileAPIView.as_view()


class FollowUserAPI(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise Http404(e)
        
    def post(self, request, username, option):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            following = self.get_object(username)
            follow_obj, created = Follow.objects.get_or_create(follower=user, following=following)

            if int(option) == 0:
                follow_obj.delete()
                #if i unfollow any user then i should not see any post ofthat user in my stream
                Stream.objects.filter(user = user, following = following).delete()
                response['status'] = 200
                response['message'] = f'{user} unfollowed {following}'
            else:
                posts = Post.objects.filter(user=following).order_by('-created_at')[:10]
                
                with transaction.atomic():
                    for post in posts:
                        stream = Stream(post=post, user=user, date=post.created_at, following=following)
                        stream.save()
                
                response['status'] = 200
                response['message'] = f'{user} followed {following}'

            return Response(response, status=status.HTTP_200_OK)
        
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("FollowUserAPI %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'userAuth'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

FollowUser = FollowUserAPI.as_view()

class EditProfileAPI(APIView):

    def put(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            username = request.data.get("username", None)
            
            if username and username != user.username:
                if User.objects.filter(username=username).exists():
                    response['status'] = 400
                    response['message'] = 'Username already exists'
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                user.username = username
                user.save()

            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 200
                response['message'] = 'Success'
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("EditProfileAPI %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'userAuth'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
EditProfile = EditProfileAPI.as_view()