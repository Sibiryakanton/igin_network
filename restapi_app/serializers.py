from django.contrib.auth.models import User
from rest_framework import serializers
from profiles_app.models import ProfileModel, Country
from django.shortcuts import get_object_or_404


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('title', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('url', 'pk', 'first_name', 'last_name', 'birthdate', 'country', 'phone', 'linkedin', 'short_status')


class AddFriendSerializer(serializers.Serializer):
    user_pk = serializers.IntegerField()
    friend_pk = serializers.IntegerField()

    def validate(self, data):
        queryset = ProfileModel.objects.all()
        errors = {}
        if data['user_pk'] == data['friend_pk']:
            errors['user_pk'] = SELF_FRIEND_ERROR
        user = get_object_or_404(queryset, pk=data['user_pk'])
        if user is None:
            errors['user_pk'] = PROFILE_404
        friend = get_object_or_404(queryset, pk=data['friend_pk'])
        if friend is None:
            errors['friend_pk'] = PROFILE_404
        if errors:
            raise serializers.ValidationError(errors)
        return super(AddFriendSerializer, self).validate(data)
