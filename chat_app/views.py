# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import ChatRoomModel, ChatMessageModel
from django.utils.safestring import mark_safe
from django.utils import timezone
import json

import pytz
from main_app.models import Astrologer, CustomerModel
from api_app.utils import get_nickname


class TestChatIndexView(View):
    def get(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        if request.user.is_anonymous:
            return render(request, 'messenger_index.html', {'client_ip': client_ip, 'chats_info': {}})
        chats = ChatRoomModel.objects.filter(members=request.user).order_by('last_updated_date')
        response = {}
        response.update({'current_user_id': request.user.id})
        response['chats'] = []
        for chat in chats:
            last_message = ChatMessageModel.objects.filter(chatroom=chat).order_by('-published_date').first()
            if last_message:
                profile_type = 'administrator'
                profile_check = request.user
                try:
                    profile_check = Astrologer.objects.get(user__id=last_message.author.id)
                    profile_type = 'astrologer'
                except Astrologer.DoesNotExist:
                    pass
                try:
                    profile_check = CustomerModel.objects.get(user__id=last_message.author.id)
                    profile_type = 'subscriber'
                except CustomerModel.DoesNotExist:
                    pass
                chat_info_elem = {'message': last_message.message,'published_date': last_message.published_date,
                                        'author_nickname': get_nickname(last_message.author)[0], 'chat_id': chat.id,
                                        'author_user_id': last_message.author.id, 'author_profile_type': profile_type,
                                        'author_profile_id': profile_check.pk, 'read': last_message.read}
            else:
                for member in chat.members.all():
                    if member != request.user:
                        chat_info_elem = {'message': None,'published_date': None,
                                                'author_nickname': get_nickname(member)[0], 'chat_id': chat.id,
                                                'author_user_id': None, 'author_profile_type': None,
                                                'author_profile_id': None, 'read': None}
            response['chats'].append(chat_info_elem)
        return render(request, 'messenger_index.html', {'client_ip': client_ip, 'chats_info': response})


class TestChatRoomView(View):
    def get(self, request, room_name):
        return render(request, 'new_chat.html', {'room_name_json': mark_safe(json.dumps(room_name))})
