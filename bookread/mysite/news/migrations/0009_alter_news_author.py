# Generated by Django 3.2.13 on 2022-08-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.CharField(blank=True, max_length=150, verbose_name='Автор'),
        ),
    ]