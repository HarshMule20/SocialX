from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True)
    mobile = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
