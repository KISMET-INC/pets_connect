# Generated by Django 2.2.4 on 2020-12-29 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0014_auto_20201225_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', to='app_one.User'),
        ),
    ]
