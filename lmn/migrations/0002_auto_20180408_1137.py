# Generated by Django 2.0.3 on 2018-04-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='venue',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
