# Generated by Django 4.0.3 on 2022-04-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='email',
        ),
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
