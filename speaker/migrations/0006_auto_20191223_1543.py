# Generated by Django 2.2.7 on 2019-12-23 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speaker', '0005_auto_20191223_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='oneDayPrice',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='twoDayPrice',
        ),
    ]
