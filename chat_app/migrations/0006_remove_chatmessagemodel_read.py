# Generated by Django 2.0.7 on 2018-08-08 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0005_chatmessagemodel_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessagemodel',
            name='read',
        ),
    ]
