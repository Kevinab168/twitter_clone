# Generated by Django 3.0.8 on 2020-07-27 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('make_posts', '0015_auto_20200727_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='content',
        ),
    ]
