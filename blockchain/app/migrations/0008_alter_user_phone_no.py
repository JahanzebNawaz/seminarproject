# Generated by Django 3.2.8 on 2021-10-26 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211020_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?46?\\d{8,15}$')]),
        ),
    ]
