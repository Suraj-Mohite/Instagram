from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .constants import GET_MESSAGE
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Tag, Follow, Stream
from .utils import get_tag_list_from_caption
from .serializers import PostSerializer, FollowSerializer, TagSerializer, StreamSerializer


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
            print(request.data)
            serializer = PostSerializer(data = request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response['status'] = 200
                response['message'] = 'Success'
                response['data'] = serializer.data
            else:
                response['message'] = serializer.errors
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("CreatePostAPIView %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

CreatePostAPI = CreatePostAPIView.as_view()

# def index(request):
        
#     if request.method == 'GET':
#         try:
#             response = {}
#             response['status'] = 500
#             response['message'] = 'Internal server error'
#             response['csrf'] = get_token(request)

#             user = request.user
#             user = User.objects.get(username='admin')
#             logger.info("##########"+ str(user), extra={'AppName': 'post'})
#             streams = Stream.objects.filter(user=user)
#             streamed_post_id_list = []
#             for stream_post in streams:
#                 streamed_post_id_list.append(str(stream_post.post.id))

#             logger.info("##########"+ str(streamed_post_id_list), extra={'AppName': 'post'})

#             posts = Post.objects.filter(id__in=streamed_post_id_list).order_by("-created_at")

#             fields_to_include = ['id', 'created_at', 'updated_at', 'picture', 'likes']

#             data = {
#                 'data' : list(posts.values(*fields_to_include))
#             }

#             response['data'] = data
#             return JsonResponse(response, status=200, encoder=DjangoJSONEncoder)

#         except Exception as e:
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 logger.error("index %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
#                 return JsonResponse(response, status=500)

# def create_post(request):
#     if request.method == 'GET':
#         try:
#             response = {}
#             response['status'] = 500
#             response['message'] = GET_MESSAGE
#             response['csrf'] = get_token(request)

#             return JsonResponse(response, status=200)

#         except Exception as e:
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 logger.error("create_post %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
#                 return JsonResponse(response, status=500)
        
#     if request.method == 'POST':
#         try:
#             response = {}
#             response['status'] = 500
#             response['message'] = "internal server error"
            
#             user = request.user
#             user = User.objects.get(username='admin')
#             logger.info("##########"+ str(user), extra={'AppName': 'post'})

            

#             return JsonResponse(response, status=200)

#         except Exception as e:
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 logger.error("create_post %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'post'})
#                 return JsonResponse(response, status=500)
