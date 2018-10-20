# coding=utf-8
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from celery import task

from api_app.error_descriptions import CHATROOM_404, CHATROOM_403, ANONYMOUS_USER
from api_app.utils import get_nickname
from main_app.models import Astrologer, CustomerModel

from .models import ChatRoomModel, ChatMessageModel

from datetime import date, datetime, time, timedelta
import json


hello_template = 'Здравствуйте, меня зовут Имя Фамилия, я потомственный астролог бла бла'
AUTORESPONDER_DICT = {'привет': hello_template,
                      'здравствуйте': hello_template,
                      'добрый день': hello_template,
                      'рад знакомству': hello_template}


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_{}'.format(self.room_name)
        self.user = self.scope['user']

        check_room = self.check_room_access()
        if check_room:
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
        nickname = get_nickname(message_obj.author)[0]
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
        nickname = get_nickname(self.user)[0]

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
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_message',
                'message_type': 'update_message_status',
                'message_id': message_obj.pk,
                'chat_id': message_obj.chatroom.pk,
                'author_id': message_obj.author.pk,
                'current_user_id': current_user_pk,
                'read': message_obj.read,
            }
        )

    def update_message(self, event):
        read = event['read']
        message_id = event['message_id']
        message_type = event['message_type']
        author_id = event['author_id']
        chat_id = event['chat_id']
        current_user_id = event['current_user_id']
        self.send(text_data=json.dumps({
            'message_id': message_id,
            'author_id': author_id,
            'current_user_id': current_user_id,
            'chat_id': chat_id,
            'read': read,
            'message_type': message_type,
        }))

    def check_room_access(self):
        date_attr = timezone.now()
        date_published = '{}-{}-{}'.format(date_attr.year, date_attr.month, date_attr.day)
        time_published = '{}:{}:{}'.format(date_attr.hour, date_attr.minute, date_attr.second)
        try:
            self.room_object = ChatRoomModel.objects.get(pk=self.room_name)

            if self.user in self.room_object.members.all():
                return self.room_object
            else:
                if self.user.is_anonymous:
                    async_to_sync(self.channel_layer.send)(
                        self.channel_name,
                        {
                            'type': 'chat_message',
                            'message_type': 'create_message',
                            'message': ANONYMOUS_USER,
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
                async_to_sync(self.channel_layer.send)(
                    self.channel_name,
                    {
                        'type': 'chat_message',
                        'message_type': 'create_message',
                        'message': CHATROOM_403,
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
        except ChatRoomModel.DoesNotExist:
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'chat_message',
                    'message_type': 'create_message',
                    'message': CHATROOM_404,
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


class MessageCounterConsumer(WebsocketConsumer):
    def connect(self):
        # Собираем список комнат для подключения. Плюс отправляем на клиент счетчики сообщений:
        # сначала по каждому диалогу в отдельности, затем сумму
        print('connect')
        self.user = self.scope['user']
        rooms_list = self.collect_chat_list()
        unread_messages_sum = 0
        for room in rooms_list:
            room_group_name = 'chat_{}'.format(room)
            async_to_sync(self.channel_layer.group_add)(
                room_group_name,
                self.channel_name,
            )
            unread_messages = ChatMessageModel.objects.filter(chatroom__pk=room, read=False).exclude(author=self.user)
            unread_messages_sum += len(unread_messages)
            self.send_chat_counter(len(unread_messages), room)
        self.send_sum_counter_number(unread_messages_sum)
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')
        rooms_list = self.collect_chat_list()
        for room in rooms_list:
            room_group_name = 'chat_{}'.format(room)
            async_to_sync(self.channel_layer.group_discard)(
                room_group_name,
                self.channel_name,
            )

    def send_sum_counter_number(self, unread_messages_sum):
        #Отправляем сумму непрочитанных сообщений для общего счетчика
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'set_sum_counter',
                'unread_messages_sum': unread_messages_sum,
                'message_type': 'set_sum_counter',
                'chat_id': None,
            }
        )

    def send_chat_counter(self, message_count, room_id):
        # Отправка непрочитанных сообщений по конкретному диалогу
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'set_sum_counter',
                'message_type': 'chat_counter',
                'unread_messages_sum': message_count,
                'chat_id': room_id,
            }
        )

    def set_sum_counter(self, event):
        #Общая функция-отправитель для счетчиков
        unread_messages_sum = event['unread_messages_sum']
        chat_id = event['chat_id']
        message_type = event['message_type']
        self.send(text_data=json.dumps({
            'message_type': message_type,
            'unread_messages_sum': unread_messages_sum,
            'chat_id': chat_id,
        }))


    def chat_message(self, event):
        #Обработчик события chat_message (нам нужно обновлять счетчики при появлении нового сообщения)
        author_id = event['author_id']
        chat_id = event['chat_id']
        if self.user.pk != author_id:
            self.send(text_data=json.dumps({
                'message_type': 'create_message',
                'chat_id': chat_id,
            }))

    def update_message(self, event):
        # Обработчик события update_message (нам нужно обновлять счетчики при обновлении статуса старого сообщения)
        author_id = event['author_id']
        chat_id = event['chat_id']
        if self.user.pk != author_id:
            self.send(text_data=json.dumps({
                'message_type': 'update_message_status',
                'chat_id': chat_id,
            }))

    def collect_chat_list(self):
        #Сбор всех чатов, в которых состоит пользователь
        rooms_list = []
        if not self.user.is_anonymous:
            chats = ChatRoomModel.objects.filter(members=self.user).order_by('-last_updated_date')
            for chat in chats:
                rooms_list.append(chat.id)
        return rooms_list
