from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


from userAuth.models import Profile
from .utils import get_tag_list_from_caption
from .models import Post, Tag, Follow, Stream, Likes, SavedPost
from .serializers import PostSerializer, FollowSerializer, TagSerializer, StreamSerializer, LikesSerializer, SavedPostSerializer
from userAuth.serializers import ProfileSerializer

import logging
import sys
import json

logger = logging.getLogger(__name__)
# Create your views here.

class IndexAPIView(APIView):
    def get(self, request, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            stream = Stream.objects.filter(user=user)
            serialized_data = StreamSerializer(stream, many=True)

            response['status'] = 200
            response['message'] = 'Success'
            response['data'] = serialized_data.data

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("IndexAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    
IndexAPI = IndexAPIView.as_view()

class CreatePostAPIView(APIView):
    def post(self, request, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            serializer = PostSerializer(data = request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response['status'] = 200
                response['message'] = 'Success'
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response['status'] = 400
                response['message'] = 'Bad Request'
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        except serializers.ValidationError as e:
                response['status'] = 400
                response['message'] = 'Bad Request'
                response['error'] = e.detail
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("CreatePostAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("CreatePostAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

CreatePostAPI = CreatePostAPIView.as_view()


class PostDetailAPIView(APIView):
     
    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist as e:
            raise Http404(e)
     
    def get(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            post = self.get_object(id)
            serializer = PostSerializer(post)
            response['status'] = 200
            response['message'] = 'Success'
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("PostDetailAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            post = self.get_object(id)
            serializer = PostSerializer(post, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response['status'] = 200
                response['message'] = 'Success'
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['status'] = 400
                response['message'] = 'Bad Request'
                response['error'] = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        except serializers.ValidationError as e:
            response['status'] = 400
            response['message'] = 'Bad Request'
            response['error'] = e.detail
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("PostDetailAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("PostDetailAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            post = self.get_object(id)
            post.delete()
            response['status'] = 200
            response['message'] = 'Success'
            return Response(response, status=status.HTTP_200_OK)
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("PostDetailAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
PostDetailAPI = PostDetailAPIView.as_view()


class LikeAPIView(APIView):
    
    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist as e:
            raise Http404(e)
        
    def post(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            if user.is_authenticated:
                post = self.get_object(id)
                
                current_likes = post.like

                likes = Likes.objects.filter(user=user, post=post)
                if not likes:
                    serializer = LikesSerializer(data={'user': user.id, 'post': id}, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        Likes.objects.create(user=user, post=post)
                        current_likes+=1
                    else:
                        response['status'] = 400
                        response['message'] = 'Bad Request'
                        response['error'] = serializer.errors
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                else:
                    Likes.objects.filter(user=user, post=post).delete()
                    current_likes-=1
                
                post.like = current_likes
                post.save()
                # serializer = PostSerializer(post)
                response['status'] = 200
                response['message'] = 'Success'
                # response['data'] = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LikeAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

LikeAPI = LikeAPIView.as_view()

class SavePostAPIView(APIView):

    def get_object(self, id):
            try:
                return Post.objects.get(id=id)
            except Post.DoesNotExist as e:
                raise Http404(e)
        
    def post(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            print(user)
            if user.is_authenticated:
                post = self.get_object(id)
                profile = Profile.objects.get(user=user)
                if profile.favourite.filter(id=id).exists():
                    profile.favourite.remove(post)
                else:
                    profile.favourite.add(post)

                profile.save()
                serializer = ProfileSerializer(profile)
                response['status'] = 200
                response['message'] = 'Success'
                response['data'] = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SavePostAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


SavePostAPI = SavePostAPIView.as_view()


class SavePostNewAPIView(APIView):

    def get_object(self, id):
            try:
                return Post.objects.get(id=id)
            except Post.DoesNotExist as e:
                raise Http404(e)
        
    def post(self, request, id, format=None):
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server error'

        try:
            user = request.user
            print(user)
            if user.is_authenticated:
                post = self.get_object(id)
                profile = Profile.objects.get(user=user)

                try:
                    saved_post_obj = SavedPost.objects.get(profile=profile, post=post)
                    saved_post_obj.delete()
                    response['status'] = 200
                    response['message'] = 'Success'
                except SavedPost.DoesNotExist as e:
                    serializer = SavedPostSerializer(data={'profile': profile.id, 'post':id})
                    if serializer.is_valid():
                        serializer.save()

                        response['status'] = 200
                        response['message'] = 'Success'
                        response['data'] = serializer.data
                    else:
                        response['status'] = 400
                        response['message'] = 'Bad Request'
                        response['error'] = serializer.errors
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                return Response(response, status=status.HTTP_200_OK)
            return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404 as e: 
            response['status'] = 404
            response['message'] = 'Failed'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SavePostNewAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


SavePostNewAPI = SavePostNewAPIView.as_view()