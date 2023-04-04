# Generated by Django 4.1.7 on 2023-04-03 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_savedpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedpost',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]