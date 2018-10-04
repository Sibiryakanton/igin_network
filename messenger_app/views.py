from django.shortcuts import render
from django.views.generic import View
from .models import ChatRoomModel, ChatMessageModel
from django.utils.safestring import mark_safe
import json

class ChatView(View):
    def get(self, request, chat_id):
        chat = ChatRoomModel.objects.get(id=chat_id)
        messages = ChatMessageModel.objects.filter(chatroom=chat).order_by('-date_published')

        messages = messages if len(messages) < 10 else messages[:10]

        return render(request, 'chatroom.html', {'messages': messages})


class TestChatIndexView(View):
    def get(self, request):
        return render(request, 'messenger_index.html', {})


class TestChatRoomView(View):
    def get(self, request, room_name):
        return render(request, 'messenger_room.html', {'room_name_json': mark_safe(json.dumps(room_name))})