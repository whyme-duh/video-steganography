# Generated by Django 4.2.5 on 2024-01-16 03:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageSteg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageencoding',
            name='image_file',
            field=models.FileField(null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name=''),
        ),
    ]
