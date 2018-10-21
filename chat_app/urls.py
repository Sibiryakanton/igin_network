from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('profiles/', views.ProfileListView.as_view(), name='profiles_list'),
    path('', views.ChatListView.as_view(), name='chats_list'),
    path('create_chat/<int:profile_id>', views.CreateChatRoomView.as_view(), name='create_chat'),

    path('chats/<str:room_name>/', views.ChatBotRoomView.as_view(), name='chat_room'),
    path('', views.ChatListView.as_view(), name='chats_list'),

]
