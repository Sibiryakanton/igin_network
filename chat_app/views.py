# coding=utf-8
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.utils import timezone

from profiles_app.models import ProfileModel
from restapi_app.error_descriptions import PROFILE_404
from .models import ChatRoomModel, ChatMessageModel

import json
import pytz


class ProfileListView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'messenger_index.html', {'profiles': {}})
        profiles = ProfileModel.objects.exclude(user=request.user)
        return render(request, 'messenger_profiles.html', {'profiles': profiles})


class ChatListView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'messenger_index.html', {'chats_list': {}})
        chats_list = ChatRoomModel.objects.filter(members=request.user).order_by('last_updated_date')
        return render(request, 'messenger_index.html', {'chats_list': chats_list})


class CreateChatRoomView(View):
    def get(self, request, profile_id):
        try:
            profile = ProfileModel.objects.get(pk=profile_id)
        except ProfileModel.DoesNotExist:
            raise ValidationError(PROFILE_404)
        chatroom = ChatRoomModel.objects.filter(members=request.user).filter(members=profile.user)
        if not len(chatroom):
            chatroom = ChatRoomModel()
            chatroom.save()
            chatroom.members.add(request.user)
            chatroom.members.add(profile.user)
            chatroom.save()
        else:
            chatroom = chatroom[0]
        return redirect(reverse('chat_room', args=[chatroom.pk]))


class ChatBotRoomView(View):
    def get(self, request, room_name):
        chatroom = ChatRoomModel.objects.get(pk=room_name)
        room_name = mark_safe(json.dumps(room_name))
        return render(request, 'chat.html', {'chatroom': chatroom, 'room_name_json': room_name})
