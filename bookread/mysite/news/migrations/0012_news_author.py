# Generated by Django 3.2.13 on 2022-08-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_remove_news_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Автор'),
        ),
    ]
