# Generated by Django 3.1 on 2020-11-13 14:53

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticPages', '0008_standstar'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст на странице - Стать участником')),
            ],
        ),
    ]
