from django.urls import path, include
from rest_framework import routers

from .viewsets import ProfileViewSet, CountryViewSet

router = routers.DefaultRouter()
router.register(r'users', ProfileViewSet)
router.register(r'country-detail', CountryViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]