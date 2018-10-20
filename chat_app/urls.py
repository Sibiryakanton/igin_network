from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:room_name>/', views.TestChatRoomView.as_view(), name='chat_room'),
    path('', views.TestChatIndexView.as_view(), name='chat_index'),

]
