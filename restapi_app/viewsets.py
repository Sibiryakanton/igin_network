from django.contrib.auth.models import User
from rest_framework import viewsets

from profiles_app.models import ProfileModel, Country

from .serializers import ProfileSerializer, CountrySerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer



class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
