# Generated by Django 5.2 on 2025-04-29 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_confirm_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passaword',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
