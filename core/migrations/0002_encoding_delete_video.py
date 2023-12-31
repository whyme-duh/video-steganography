# Generated by Django 4.2.5 on 2023-10-02 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encoding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='videos/', verbose_name='')),
                ('secret_key', models.CharField(blank=True, max_length=80, null=True)),
                ('message', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
