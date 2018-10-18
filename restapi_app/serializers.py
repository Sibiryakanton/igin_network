from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from profiles_app.models import ProfileModel, Country
from .error_descriptions import COUNTRY_404


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('url', 'title', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        errors = dict()
        try:
            if data.get('country') != None:
                Country.objects.get(pk=data.get('country'))
        except Country.DoesNotExist:
            errors['country'] = COUNTRY_404
        if errors:
            raise serializers.ValidationError(errors)
        return super(ProfileSerializer, self).validate(data)

    class Meta:
        model = ProfileModel
        fields = ('url', 'pk', 'first_name', 'last_name', 'birthdate', 'country', 'phone', 'linkedin', 'short_status')
