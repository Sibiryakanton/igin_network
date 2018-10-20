# Generated by Django 2.0.7 on 2018-07-31 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=3000)),
                ('message_html', models.TextField()),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoomModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
        ),
        migrations.AddField(
            model_name='chatmessagemodel',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_app.ChatRoomModel'),
        ),
    ]