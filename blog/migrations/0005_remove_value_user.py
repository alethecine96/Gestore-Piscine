# Generated by Django 3.1 on 2020-09-17 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200917_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='user',
        ),
    ]
