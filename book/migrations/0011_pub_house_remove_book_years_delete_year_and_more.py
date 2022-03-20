# Generated by Django 4.0.3 on 2022-03-20 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_alter_author_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pub_house',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('email', models.CharField(max_length=70)),
                ('slug', models.SlugField(blank=True, default='')),
                ('address', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='years',
        ),
        migrations.DeleteModel(
            name='Year',
        ),
        migrations.AddField(
            model_name='book',
            name='pub_house',
            field=models.ManyToManyField(to='book.pub_house'),
        ),
    ]