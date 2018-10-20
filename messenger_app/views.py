from django.shortcuts import render
from django.views.generic import View
from django.utils.safestring import mark_safe

from .models import ChatRoomModel, ChatMessageModel
from profiles_app.models import ProfileModel
import json

class ChatView(View):
    def get(self, request, chat_id):
        chat = ChatRoomModel.objects.get(id=chat_id)
        messages = ChatMessageModel.objects.filter(chatroom=chat).order_by('-date_published')

        messages = messages if len(messages) < 10 else messages[:10]

        return render(request, 'chatroom.html', {'messages': messages})


class ChatIndexView(View):
    def get(self, request):
        profiles = ProfileModel.objects.exclude(user=request.user)
        return render(request, 'messenger_index.html', {'profiles': profiles})