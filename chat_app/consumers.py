# coding=utf-8
from django.contrib.auth.models import User
from django.utils import timezone

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import ChatRoomModel, ChatMessageModel
from profiles_app.models import ProfileModel
from restapi_app.error_descriptions import CHAT_400

from datetime import date, datetime, time, timedelta
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_{}'.format(self.room_name)
        self.user = self.scope['user']

        if self.check_room_access():
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            chat_messages = ChatMessageModel.objects.filter(chatroom=self.room_object).order_by('published_date')
            if len(chat_messages) > 30:
                chat_messages = chat_messages[len(chat_messages)-30:]
            for message_object in chat_messages:
                async_to_sync(self.send_personal_message(message_object))
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type_message = text_data_json['type_message']
        check_room = self.check_room_access()
        if check_room:
            if type_message == 'send_message':
                message = text_data_json['message']
                if message != '':
                    message_object = ChatMessageModel.objects.create(author=self.user, message=message, chatroom=self.room_object)
                    self.send_group_message(message_object, self.user.pk)

            elif type_message == 'update_message_status':
                message_id = text_data_json['message_id']
                message_object = ChatMessageModel.objects.get(pk=message_id)
                self.update_message_status(message_object, self.user.pk)

    def send_personal_message(self, message_obj):
        date_attr = message_obj.published_date
        date_published = '{}-{}-{}'.format(date_attr.year, date_attr.month, date_attr.day)
        time_published = '{}:{}:{}'.format(date_attr.hour, date_attr.minute, date_attr.second)
        profile = ProfileModel.objects.get(user=self.user)
        nickname = str(profile)
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'message_type': 'create_message',
                'message': message_obj.message,
                'date_published': date_published,
                'time_published': time_published,
                'author': nickname,
                'author_id': message_obj.author.pk,
                'message_id': message_obj.pk,
                'read': message_obj.read,
                'chat_id': message_obj.chatroom.pk,
                'current_user_id': self.user.pk,
            }
        )

    def send_group_message(self, message_obj, request_user):
        date_attr = message_obj.published_date
        date_published = '{}-{}-{}'.format(date_attr.year, date_attr.month, date_attr.day)
        time_published = '{}:{}:{}'.format(date_attr.hour, date_attr.minute, date_attr.second)
        profile = ProfileModel.objects.get(user=self.user)
        nickname = str(profile)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': 'create_message',
                'message': message_obj.message,
                'date_published': date_published,
                'time_published': time_published,
                'author': nickname,
                'author_id': message_obj.author.pk,
                'message_id': message_obj.pk,
                'read': message_obj.read,
                'chat_id': message_obj.chatroom.pk,
                'current_user_id': request_user,
            }
        )

    def chat_message(self, event):
        message = event['message']
        date_published = event['date_published']
        time_published = event['time_published']
        author = event['author']
        read = event['read']
        message_id = event['message_id']
        chat_id = event['chat_id']
        current_user_id = event['current_user_id']
        author_id = event['author_id']
        message_type = event['message_type']

        self.send(text_data=json.dumps({
            'chat_id': chat_id,
            'message': message,
            'date_published': date_published,
            'time_published': time_published,
            'author': author,
            'author_id': author_id,

            'message_id': message_id,
            'current_user_id': current_user_id,
            'read': read,
            'message_type': message_type,
        }))

    def update_message_status(self, message_obj, current_user_pk):
        message_obj.read = True
        message_obj.save()
        self.send(text_data=json.dumps({
            'message_type': 'update_message_status',
            'message_id': message_obj.pk,
            'author_id': message_obj.author.pk,
            'current_user_id': current_user_pk,
            'chat_id': message_obj.chatroom.pk,
            'read': message_obj.read,
        }))

    def check_room_access(self):
        try:
            self.room_object = ChatRoomModel.objects.get(pk=self.room_name)
            if self.user in self.room_object.members.all():
                return self.room_object
            else:
                return self.send_400_message()
        except ChatRoomModel.DoesNotExist:
            return self.send_400_message()

    def send_400_message(self):
        date_attr = timezone.now()
        date_published = '{}-{}-{}'.format(date_attr.year, date_attr.month, date_attr.day)
        time_published = '{}:{}:{}'.format(date_attr.hour, date_attr.minute, date_attr.second)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'message_type': 'create_message',
                'message': CHAT_400,
                'date_published': date_published,
                'time_published': time_published,
                'author': 'Ошибка',
                'message_id': '1',
                'chat_id': '1',
                'current_user_id': '1',
                'author_id': '1',
                'read': True,
            }
        )
        return False