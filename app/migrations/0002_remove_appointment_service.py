# Generated by Django 4.2.4 on 2023-08-26 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='service',
        ),
    ]
