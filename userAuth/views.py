from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

from django.urls import resolve
from django.http import Http404
from post.models import Post, SavedPost
from .models import Profile
from .serializers import ProfileSerializer
from post.serializers import PostSerializer, SavedPostSerializer
from django.contrib.auth.models import User

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
            
            user = self.get_object(username)
            profile_obj = Profile.objects.get(user=user)
            url_name = resolve(request.path).url_name
            if url_name == "user-posts":
                posts = Post.objects.filter(user=user).order_by('-created_at')
            elif url_name == "user-saved":
                posts = Post.objects.filter(post_saved__profile=profile_obj).order_by("-post_saved__created_at") # here post_saved is related name in SavedPost model connected post with it with foreignkey

            #Pagination
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(posts, request)
            post_serializer = PostSerializer(paginated_queryset, many=True)
            profile_serializer = ProfileSerializer(profile_obj)
            # serializer = PostSerializer(posts, many=True)

            response['status'] = 200
            response['message'] = 'Success'
            response['data']['profile'] = profile_serializer.data
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