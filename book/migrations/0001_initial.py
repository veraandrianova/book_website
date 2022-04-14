# Generated by Django 4.0.3 on 2022-04-14 11:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=70, verbose_name='имя')),
                ('lastname', models.CharField(max_length=70, verbose_name='фамилия')),
                ('image', models.ImageField(blank=True, upload_to='movies/', verbose_name='Постер')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, default='')),
                ('name', models.CharField(blank=True, max_length=70)),
            ],
            options={
                'verbose_name': 'автор',
                'verbose_name_plural': 'авторы',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='photos/', verbose_name='Постер')),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Рейтинг')),
                ('is_best_selling', models.BooleanField(blank=True, null=True)),
                ('slug', models.SlugField(default='')),
                ('is_published', models.BooleanField(default=True)),
                ('cover', models.CharField(choices=[('solid', 'Твердый переплет'), ('soft', 'Мягкий переплет')], default='solid', max_length=10, verbose_name='переплет')),
            ],
            options={
                'verbose_name': 'книга',
                'verbose_name_plural': 'книги',
            },
        ),
        migrations.CreateModel(
            name='BookPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rack', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='стелаж')),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='порядковый норме')),
            ],
            options={
                'verbose_name': 'место книги',
                'verbose_name_plural': 'места книг',
            },
        ),
        migrations.CreateModel(
            name='PubHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_house', models.CharField(max_length=70, verbose_name='название издательства')),
                ('email', models.CharField(max_length=70, verbose_name='почта')),
                ('slug', models.SlugField(blank=True, default='')),
                ('address', models.CharField(blank=True, default='', max_length=200, verbose_name='адрес')),
            ],
            options={
                'verbose_name': 'издание',
                'verbose_name_plural': 'издания',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='текст')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='измененно')),
                ('active', models.BooleanField(default=True, verbose_name='активность')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_book', to='book.book')),
            ],
            options={
                'verbose_name': 'комментрарий',
                'verbose_name_plural': 'комментарии',
                'ordering': ('created',),
            },
        ),
    ]
