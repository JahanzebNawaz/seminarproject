# Generated by Django 3.2.8 on 2021-10-27 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_proposals_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposals',
            name='files',
            field=models.FileField(default='', upload_to='uploads/proposals/%Y/%m/%d/'),
        ),
    ]
