# Generated by Django 3.2.8 on 2021-10-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20211027_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]