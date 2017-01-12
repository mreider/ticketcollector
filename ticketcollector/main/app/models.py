from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.user.username

class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    search_criteria = models.CharField(max_length=2000,null=True)
    name = models.CharField(max_length=1000,unique=True)


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    collection = models.ForeignKey(Collection,related_name="collection")
    zd_ticket_id = models.CharField(max_length=1000)
    subject = models.CharField(max_length=1000)
    requester = models.CharField(max_length=1000)
    description = models.TextField()
    created_at  = models.DateTimeField()

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket,related_name="ticket")
    zd_comment_id = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    plain_body = models.TextField()
    is_public = models.BooleanField()
