# Generated by Django 4.0.3 on 2022-04-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_author_email_author_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]