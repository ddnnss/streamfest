# Generated by Django 2.2.6 on 2020-01-06 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speaker', '0012_auto_20191225_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speaker',
            name='buys',
        ),
        migrations.AddField(
            model_name='ticket',
            name='sells',
            field=models.IntegerField(default=0, verbose_name='Всего продаж'),
        ),
    ]
