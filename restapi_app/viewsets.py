# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from profiles_app.models import ProfileModel, Country

from .serializers import ProfileSerializer, UserSerializer, CountrySerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request):
        profile_serializer = self.serializer_class(data=request.data)
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        profile_serializer.is_valid(raise_exception=True)

        new_user = self.create_user(user_serializer.validated_data)
        new_profile_id = self.create_profile(profile_serializer.validated_data, new_user)
        return Response({'id': new_profile_id})

    def create_user(self, validated_data):
        new_user = User.objects.create(username=validated_data['username'], password=validated_data['password'])
        return new_user.pk

    def create_profile(self, validated_data, new_user):
        new_user = User.objects.get(pk=new_user)
        new_profile = ProfileModel()
        new_profile.phone = validated_data['phone']
        new_profile.user = new_user
        new_profile.save()
        return new_profile.pk

    def update(self, request):
        pass

    def destroy(self, request):
        pass

    @action(detail=True, methods=['get',])
    def get_friends(self, request, **kwargs):
        profile = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if profile != None:
            friends = profile.friends.all()
            serializer = ProfileSerializer(friends, many=True, context={'request': request})
            return Response(data=serializer.data)
        else:
            return Response(data={'pk': ''})


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
