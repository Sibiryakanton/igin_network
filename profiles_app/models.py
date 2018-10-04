# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProfileModel(models.Model):
    class Meta:
        verbose_name='профиль'
        verbose_name_plural='профили'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #avatar = models.ForeignKey('images_app.ImageModel', verbose_name='Аватар', blank=True, null=True, on_delete=models.SET_NULL)
    nickname = models.CharField('Никнейм для адресной строки браузера', max_length=200, blank=True)
    birthdate = models.DateField('Дата рождения', blank=True)
    country = models.ForeignKey('Country', verbose_name='Страна', null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField('Телефон', max_length=50)
    linkedin = models.URLField('LinkedIn', max_length=150, blank=True)
    short_status = models.CharField('Статус', max_length=200, blank=True)
    friends = models.ManyToManyField('ProfileModel', verbose_name='Друзья', blank=True)
    created_date = models.DateTimeField('Дата создани профиля', default=timezone.now)

    def __str__(self):
        return '{} {}, {}'.format(self.user.first_name, self.user.last_name, self.nickname)


class Country(models.Model):
    class Meta:
        verbose_name='страна'
        verbose_name_plural='страны'

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-транслит')

    def __str__(self):
        return self.title
