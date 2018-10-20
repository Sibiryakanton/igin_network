# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework import status

from profiles_app.models import ProfileModel, Country
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, UserSerializer, CountrySerializer, AddFriendSerializer
from .error_descriptions import *

from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or view.action in ['create']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (CustomPermission,)

    def create(self, request):
        profile_serializer = self.serializer_class(data=request.data)
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        profile_serializer.is_valid(raise_exception=True)
        new_user = self.create_user(user_serializer.validated_data)
        new_profile_id = self.create_profile(profile_serializer.validated_data, new_user)
        return Response({'id': new_profile_id})

    def update(self, request, **kwargs):
        obj = get_object_or_404(self.queryset, pk=kwargs["pk"])
        obj.check_permission(request.user.pk) #check_access = self.check_profile_access(request, kwargs['pk'])
        return super(ProfileViewSet, self).update(request, **kwargs)

    def destroy(self, request, **kwargs):
        obj = get_object_or_404(self.queryset, pk=kwargs["pk"])
        obj.check_permission(request.user.pk)
        return super(ProfileViewSet, self).destroy(request, **kwargs)

    @action(detail=True, methods=['get', ])
    def get_friends(self, request, **kwargs):
        profile = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if profile is not None:
            friends = profile.friends.exclude(pk=profile.pk)
            serializer = ProfileSerializer(friends, many=True, context={'request': request})
            return Response(data=serializer.data)
        else:
            return Response(data={'pk': PROFILE_404}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post', ])
    def add_friend(self, request, **kwargs):
        obj = get_object_or_404(self.queryset, pk=kwargs["pk"])
        obj.check_permission(request.user.pk)

        user, friend = self.get_user_friend(request, **kwargs)
        user.friends.add(friend)
        user.save()
        return Response(data={'status': True})

    @action(detail=True, methods=['post', ])
    def remove_friend(self, request, **kwargs):
        obj = get_object_or_404(self.queryset, pk=kwargs["pk"])
        obj.check_permission(request.user.pk)

        user, friend = self.get_user_friend(request, **kwargs)
        user.friends.remove(friend)
        user.save()
        return Response(data={'status': True})

    def create_user(self, validated_data):
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user.pk

    def create_profile(self, validated_data, new_user):
        new_user = User.objects.get(pk=new_user)
        new_profile = ProfileModel(phone=validated_data['phone'], user=new_user)
        new_profile.save()
        new_profile.friends.add(new_profile)
        new_profile.save()
        return new_profile.pk

    def get_user_friend(self, request, **kwargs):
        profile_serializer = AddFriendSerializer(data=request.data)
        profile_serializer.is_valid(raise_exception=True)
        data = profile_serializer.validated_data
        user = ProfileModel.objects.get(pk=kwargs['pk'])
        friend = ProfileModel.objects.get(pk=data['friend_pk'])
        return user, friend


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
