from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('chatroom/<int:chat_id>/', views.ChatView.as_view(), name='chatroom'),
    path('', views.ChatIndexView.as_view(), name='chat_index'),

]
