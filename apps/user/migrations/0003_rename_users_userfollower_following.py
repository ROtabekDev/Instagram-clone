# Generated by Django 4.1.7 on 2023-04-01 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_following_userfollower_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollower',
            old_name='users',
            new_name='following',
        ),
    ]
