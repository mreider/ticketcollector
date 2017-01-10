from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.user.username