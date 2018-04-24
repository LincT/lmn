# Generated by Django 2.0.3 on 2018-04-24 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0004_auto_20180424_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='user_photo_file_name',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]