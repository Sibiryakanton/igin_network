# coding=utf-8
from django.db import models

from django.contrib.auth.models import User

class ChatRoomModel(models.Model):
    members = models.ManyToManyField(User, verbose_name='Участники')
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        members = self.members.all()
        return 'Чат участников {}'.format(', '.join([member.username for member in members]))


class ChatMessageModel(models.Model):
    chatroom = models.ForeignKey('ChatRoomModel', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    date_published = models.DateTimeField(auto_now_add=True)
