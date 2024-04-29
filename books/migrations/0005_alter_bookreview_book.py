# Generated by Django 4.0 on 2024-04-26 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_bookreview_stars_given'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='books.book'),
        ),
    ]
