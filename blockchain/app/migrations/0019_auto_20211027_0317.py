# Generated by Django 3.2.8 on 2021-10-27 03:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_proposals_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_currency', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='credit_card',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{14}$')]),
        ),
    ]