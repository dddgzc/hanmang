# Generated by Django 2.2 on 2019-11-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191126_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='salt',
            field=models.CharField(default='', max_length=32, verbose_name='盐'),
        ),
    ]
