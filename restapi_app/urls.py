from django.urls import path, include
from rest_framework import routers
from . import views
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.ProfileViewSet)
router.register(r'countries', viewsets.CountryViewSet)

urlpatterns = [
    path('auth/get_token/', views.CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
