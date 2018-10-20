# coding=utf-8
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver

class ChatRoomModel(models.Model):
    members = models.ManyToManyField(User, verbose_name='Участники')
    published_date = models.DateTimeField(default=timezone.now)
    last_updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        members = self.members.all()
        return 'Чат участников {}'.format(', '.join([member.username for member in members]))


class ChatMessageModel(models.Model):
    chatroom = models.ForeignKey('ChatRoomModel', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    published_date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField('Прочитано', default=False)

    def save(self, *args, **kwargs):
        super(ChatMessageModel, self).save(*args, **kwargs)
        update_chat_date(self, *args, **kwargs)


def update_chat_date(obj, *args, **kwargs):
    obj.chatroom.last_updated_date = timezone.now()
    obj.chatroom.save()