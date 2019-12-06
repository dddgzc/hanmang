# Generated by Django 2.2.2 on 2019-11-22 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='课程价格'),
        ),
    ]
