# Generated by Django 3.1 on 2020-09-22 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200922_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='piscina',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.piscina'),
            preserve_default=False,
        ),
    ]
