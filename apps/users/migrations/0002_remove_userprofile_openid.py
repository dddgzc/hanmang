# Generated by Django 2.1.4 on 2019-12-20 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='openid',
        ),
    ]
