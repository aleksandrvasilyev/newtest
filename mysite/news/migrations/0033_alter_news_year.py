# Generated by Django 3.2.13 on 2022-08-04 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0032_news_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='year',
            field=models.CharField(max_length=10, verbose_name='year'),
        ),
    ]