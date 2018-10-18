# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer, UserSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk})


class FriendsManagerView(APIView):
    def get(self, profile_pk):
        friends = ProfileModel.objects.get(pk=profile_pk).friends.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(data=serializer.data)
        # Получить список друзей

    def post(self):
        pass
        # Добавить/удалить пользователя из друзей
