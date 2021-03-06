# Generated by Django 2.0.7 on 2018-10-04 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='URL-транслит')),
            ],
            options={
                'verbose_name': 'страна',
                'verbose_name_plural': 'страны',
            },
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=200, verbose_name='Никнейм для адресной строки браузера')),
                ('birthdate', models.DateField(blank=True, verbose_name='Дата рождения')),
                ('phone', models.CharField(max_length=50, verbose_name='Телефон')),
                ('linkedin', models.URLField(blank=True, max_length=150, verbose_name='LinkedIn')),
                ('short_status', models.CharField(blank=True, max_length=200, verbose_name='Статус')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создани профиля')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles_app.Country', verbose_name='Страна')),
                ('friends', models.ManyToManyField(blank=True, to='profiles_app.ProfileModel', verbose_name='Друзья')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
    ]
