# Generated by Django 2.2 on 2019-11-28 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20191126_0923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='fav_name',
            new_name='fav_nums',
        ),
    ]