# coding=utf-8
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User

from .models import ChatRoomModel, ChatMessageModel

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'chat_{}'.format(self.room_name)
        self.room_object = ChatRoomModel.objects.get(pk=self.room_name)
        self.room_messages = ChatMessageModel.objects.filter(chatroom=self.room_object).order_by('date_published').values()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print('receive')

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = User.objects.get(id=text_data_json['id'])
        message_object = ChatMessageModel.objects.create(author=user, message=message, chatroom=self.room_object)
        print(text_data_json)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        print('chat_message')
        message = event['message']
        print(message)
        self.send(text_data=json.dumps({
            'message': message
        }))
