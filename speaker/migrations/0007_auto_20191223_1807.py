# Generated by Django 2.2.6 on 2019-12-23 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('speaker', '0006_auto_20191223_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Сумма'),
        ),
        migrations.AddField(
            model_name='order',
            name='streamer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='speaker.Speaker', verbose_name='Билет от'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена билета. Эта цена будет применена ко всем билетам'),
        ),
    ]