# Generated by Django 4.1.7 on 2023-04-01 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_chat_participant_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
