# Generated by Django 4.1.7 on 2023-02-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_info',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
