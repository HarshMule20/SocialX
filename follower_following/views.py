# Django imports
from django.db.models import Q

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models import
from .models import FollowerFollowingModel
from user.models import User


class Following(APIView):
    @staticmethod
    def post(request):
        try:
            FollowerFollowingModel.objects.get(following=request.data['following'], follower=request.user.id)
            return Response({'error':'You have already followed the particular user'}, status=status.HTTP_200_OK)
        except FollowerFollowingModel.DoesNotExist:
            if request.data['following'] is not request.user.id:
                request.data['follower'] = request.user
                request.data['following'] = User.objects.get(id=request.data['following'])
                follower_following_obj = FollowerFollowingModel(**request.data)
                follower_following_obj.save()
                return Response({'message':'user followed successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)


class FollowerFollowing(APIView):
    @staticmethod
    def get(request):
        follower_following_obj = FollowerFollowingModel.objects.filter(
            Q(following=request.user.id) | Q(follower=request.user.id)
        )
        follower_list = []
        following_list = []
        for single in follower_following_obj:
            if single.following.id == request.user.id:
                follower_list.append({
                    'user_id':single.follower.id,
                    'username':single.follower.username,
                    'no_of_followers': FollowerFollowingModel.objects.filter(
                        following=single.follower.id).count(),
                    'no_of_following': FollowerFollowingModel.objects.filter(
                        follower=single.follower.id).count(),
                    'first_name': single.follower.first_name,
                    'last_name': single.follower.last_name

                })
                print("follower = ", follower_list)
            else:
                following_list.append({
                    'user_id': single.following.id,
                    'username': single.following.username,
                    'no_of_followers': FollowerFollowingModel.objects.filter(
                        following=single.following.id).count(),
                    'no_of_following': FollowerFollowingModel.objects.filter(
                        follower=single.following.id).count(),
                    'first_name': single.following.first_name,
                    'last_name': single.following.last_name
                })
                print("following = ",following_list)
        return Response({'follower':follower_list, 'following':following_list}, status=status.HTTP_200_OK)


class Unfollow(APIView):
    @staticmethod
    def post(request):
        following_obj = FollowerFollowingModel.objects.get(following=request.data['following'], follower=request.user.id)
        following_obj.delete()
        return Response({'user unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)