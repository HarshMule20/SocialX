from django.utils import timezone
from rest_framework import serializers

# models imports
from .models import MessageModel


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['sender', 'receiver', 'message', 'created_at', 'updated_at', 'conversation_id']

    def to_representation(self, instance):
        return {
            "sender": instance.sender.username,
            "receiver": instance.receiver.username,
            "message": instance.message,
            "conversation_id": instance.conversation_id,
            "created_at": instance.created_at,
        }

    # def update(self, instance, validated_data):
    #     instance.message = validated_data.get('message', instance.message)
    #     instance.updated_at = timezone.now()
    #     instance.save()
    #     return instance
