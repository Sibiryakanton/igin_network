from django.contrib import admin
from .models import *


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'last_updated_date')
    list_display_links = ('pk', '__str__',)
    list_per_page = 50
    ordering = ['-pk']
    search_field = ['pk', '__str__']
    exclude = ()


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'chatroom', 'author', 'published_date', 'message')
    list_display_links = ('pk', 'message')
    list_per_page = 50
    ordering = ['-pk']
    search_field = ['pk']
    exclude = ()


admin.site.register(ChatRoomModel, ChatRoomAdmin)
admin.site.register(ChatMessageModel, ChatMessageAdmin)
