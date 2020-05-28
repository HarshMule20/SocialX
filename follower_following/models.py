from django.db import models
from user.models import User
from django.utils import timezone


class FollowerFollowingModel(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", null=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_accept = models.BooleanField(default=True)

    class Meta:
        db_table = "follower_following"
