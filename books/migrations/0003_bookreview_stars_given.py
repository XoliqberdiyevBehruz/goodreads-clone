# Generated by Django 4.0 on 2024-04-26 02:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='stars_given',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxLengthValidator(5)]),
        ),
    ]
