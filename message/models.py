from django.db import models
from django.utils import timezone
from user.models import User


class MessageModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField(null=True, blank=True)
    conversation_id = models.CharField(max_length=30, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_messages"

    def generate_conversation_id(self):
        sender = self.sender
        receiver = self.receiver
        if sender.id > receiver.id:
            sender, receiver = receiver, sender
        conv_id = str(sender.id) + '_' + str(receiver.id)
        return conv_id

    def save(self, *args, **kwargs):
        if not self.conversation_id:
            self.conversation_id = self.generate_conversation_id()
        super().save(*args, **kwargs)
