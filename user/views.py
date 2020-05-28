import logging

# DRF import
from django.db.models import Q

from rest_framework.settings import api_settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# models import
from .models import User
from follower_following.models import FollowerFollowingModel

# serializer imports
from .serializer import UserSerializer

# helper import
from Auth.token import token_encode, token_decode
from .helper import validate_password

logger = logging.getLogger(__name__)


class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        logger.info('In signup')
        try:
            user = User.objects.get(username=request.data['username'], is_active=True)
            token = token_encode(user)
            return Response({'token': token, 'message': 'Username already exist', 'user': UserSerializer(user).data},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            request.data['password'] = make_password(validate_password(request.data['password']))
            user_srlzr = UserSerializer(data=request.data)
            try:
                user_srlzr.is_valid(raise_exception=True)
                user_srlzr.save()
            except Exception as e:
                logger.error(e)
            print(user_srlzr.instance)
            token = token_encode(user_srlzr.instance)
            print(token)
            return Response({'token': token, 'User': user_srlzr.data}, status=status.HTTP_201_CREATED)


class Profile(APIView):

    @staticmethod
    def get(request):
        user = User.objects.get(id=request.user.id)
        user_srlzer = UserSerializer(user)
        return Response({'user': user_srlzer.data}, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        user = User.objects.get(id=request.user.id)
        if 'gender' in request.data.keys():
            if request.data['gender'].lower() != 'male' and request.data['gender'].lower() != 'female':
                return Response({'error': 'gender field is invalid.'}, status=status.HTTP_404_NOT_FOUND)
        user_srlzer = UserSerializer(user, data=request.data, partial=True)
        user_srlzer.is_valid(raise_exception=True)
        user_srlzer.save()
        return Response({'user': user_srlzer.data}, status=status.HTTP_200_OK)


class UserList(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        query = request.GET.get('username', '')
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        if query:
            user_obj = User.objects.filter(
                Q(username__istartswith=query)| Q(first_name__istartswith=query)
            )
        else:
            user_obj = User.objects.all().order_by('-id')
        user_srlzer = UserSerializer(user_obj, many=True)
        page = paginator.paginate_queryset(user_srlzer.data, request)
        return paginator.get_paginated_response(page)

class UserLogin(APIView):
    @staticmethod
    def post(request):
        user_obj = User.objects.get(Q(username=request.data['username']) | Q(email=request.data['username']))
        if user_obj.check_password(request.data['password']):
            token = token_encode(user_obj)
            return Response({'messsage': 'user login successfully', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'invalid username or password'}, status=status.HTTP_200_OK)

class Logout(APIView):
    @staticmethod
    def get(request):
        User.objects.filter(id=request.user.id).update(last_login=timezone.localtime())
        return Response({'message': 'User logged out successfully'},status=status.HTTP_200_OK)

class UserAutoComplete(APIView):
    @staticmethod
    def post(request):
        user_objs = User.objects.filter(Q(username__istartswith=request.data['name']))
        user_list = []
        for user_obj in user_objs:
            user_list.append({
                'id': user_obj.id,
                'name': user_obj.username
            })
        return Response(user_list, status=status.HTTP_200_OK)

class SearchInFollowerFollowing(APIView):
    @staticmethod
    def get(request):
        query = request.GET.get('username', '')
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        if query:
            user_objs = User.objects.filter(
                Q(username__istartswith=query)| Q(first_name__istartswith=query)
            )
            for user_obj in user_objs:
                follower_following_obj = FollowerFollowingModel.objects.get(Q(following=user_obj.id) & Q(follower=request.user.id))
            user_srlzer = UserSerializer(user_objs, many=True).data
            page = paginator.paginate_queryset(user_srlzer, request)
            return paginator.get_paginated_response(page)
        else:
            data_list = []
            
            follower_obj = FollowerFollowingModel.objects.filter(Q(following=request.user.id))
            following_obj = FollowerFollowingModel.objects.filter(Q(follower=request.user.id))
            print("follower_following: ",follower_obj)
            for follower in follower_obj:
                data_list.append({
                'user_srlzer': UserSerializer(follower.follower).data
                })
            for following in following_obj:
                data_list.append({
                'user': UserSerializer(following.following).data
                })
            print("data_list", data_list)
            page = paginator.paginate_queryset(data_list, request)
            return paginator.get_paginated_response(page)
