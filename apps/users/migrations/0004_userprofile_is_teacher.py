# Generated by Django 2.1.4 on 2019-12-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_openid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='是否是老师'),
        ),
    ]
