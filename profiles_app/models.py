# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

from restapi_app.error_descriptions import *


class ProfileModel(models.Model):
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    first_name = models.CharField(max_length=30, default='Аноним')
    last_name = models.CharField(max_length=150, default='Аноним')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField('Никнейм для адресной строки браузера', max_length=200, blank=True)
    birthdate = models.DateField('Дата рождения', null=True, blank=True,)
    country = models.ForeignKey('Country', verbose_name='Страна', null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.CharField('Номер телефона', max_length=20, unique=True,
                             validators=[RegexValidator(regex='^[0-9]{9,16}$',
                                                        message=PHONE_400
                                                        ),
                                         ]
                             )
    linkedin = models.URLField('LinkedIn', max_length=150, blank=True)
    short_status = models.CharField('Статус', max_length=200, blank=True)
    friends = models.ManyToManyField('ProfileModel', verbose_name='Друзья', blank=True)
    created_date = models.DateTimeField('Дата создания профиля', default=timezone.now)

    def return_default_id(self):
        return 'id{}'.format(self.pk)

    def __str__(self):
        return '{} {}, {}'.format(self.first_name, self.last_name, self.nickname or self.return_default_id())


class Country(models.Model):
    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-транслит')

    def __str__(self):
        return self.title
