from django.contrib.auth.models import User
from rest_framework import serializers

from profiles_app.models import ProfileModel, Country




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('title', 'slug')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = ProfileModel
        fields = ('url', 'birthdate', 'country', 'phone', 'short_status')




