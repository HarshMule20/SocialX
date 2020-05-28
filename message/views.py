import logging

# Django Imports
from operator import attrgetter

from django.utils import timezone
from django.db.models import Q, Sum, Count

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models imports
from user.models import User
from .models import MessageModel

# Serializer imports
from .serializers import MessageSerializer

logger = logging.getLogger(__name__)


class MessageMgmt(APIView):

    @staticmethod
    def post(request, username):
        try:
            print(request)
            request.data['sender'] = request.user.id

            request.data['receiver'] = User.objects.get(username=username).id
            print(request.data)
            message_srlzer = MessageSerializer(data=request.data)
            try:
                message_srlzer.is_valid(raise_exception=True)
                message_srlzer.save()
            except Exception as e:
                logger.error(e)
            return Response(message_srlzer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get(request, username):
        try:
            message_obj = MessageModel.objects.filter(sender=request.user.id,
                                                      receiver=User.objects.get(username=username).id,
                                                      is_active=True).order_by('-created_at')
            print(message_obj)
            message_srlzer = MessageSerializer(message_obj, many=True)
            return Response(message_srlzer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)

    # @staticmethod
    # def put(request, username, msgid=None):
    #     try:
    #         message_obj = MessageModel.objects.get(id=msgid, is_active=True)
    #         # try:
    #         #     message_srlzer.is_valid()
    #         #     message_srlzer.save()
    #         # except Exception as e:
    #         #     logger.error(e)
    #         message_obj.message = request.data['message']
    #         message_obj.updated_at = timezone.now()
    #         message_obj.save()
    #         message_srlzer = MessageSerializer(message_obj)
    #         return Response({'success': 'message updated successfully', 'message': message_srlzer.data},
    #                         status=status.HTTP_200_OK)
    #     except MessageModel.DoesNotExist:
    #         return Response({'error': 'Message does not exists'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, username, msgid=None):
        try:
            message_obj = MessageModel.objects.get(id=msgid, is_active=True)
            message_obj.is_active = False
            message_obj.updated_at = timezone.now()
            message_obj.save()
            return Response({'success': 'message deleted successfully'}, status=status.HTTP_200_OK)
        except MessageModel.DoesNotExist:
            return Response({'error': 'Message does not exists'}, status=status.HTTP_404_NOT_FOUND)


class RecentMessages(APIView):
    @staticmethod
    def get_id(obj):
        return obj.id

    # def __repr__(self):
    #     return '{}: {} {}'.format(self.__class__.__name__,
    #                               self.id,
    #                               self.conversation_id)

    # def __cmp__(self, other):
    #     if hasattr(other, 'id'):
    #         return self.id.__cmp__(other.id)

    @staticmethod
    def get(request):
        message_obj = MessageModel.objects.filter(Q(sender=request.user.id, is_active=True) |
                                                  Q(receiver=request.user.id, is_active=True)).\
            order_by('conversation_id','-id').distinct('conversation_id')
        result = sorted(message_obj, key=RecentMessages.get_id, reverse=True)
        print('lst : ', result)
        message_srlzer = MessageSerializer(result, many=True)
        return Response(message_srlzer.data, status=status.HTTP_200_OK)
