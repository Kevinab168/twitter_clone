# Generated by Django 3.0.8 on 2020-07-20 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_posts', '0008_auto_20200718_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='make_posts.Follower'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
