from django.shortcuts import render
from .models import *

# Create your views here.

# Вьюха главной страницы: редирект на страницу авторизации либо на список чатов


# Вьюха чата

# Вьюха страницы пользователя


def index(request):
    all_countries = Country.objects.all()
    return render(request, 'index.html', {'all_countries': all_countries})