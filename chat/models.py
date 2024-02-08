
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Chat(models.Model):
    name = models.CharField(max_length=99, blank=False, null=False)
    members = models.ManyToManyField(User, related_name='chat_member')


# class ChatMember(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     # class Meta:
#     #     db_table = 'chat_chat_members'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)

