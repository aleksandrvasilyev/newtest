# Generated by Django 3.2.13 on 2022-08-04 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0033_alter_news_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='idflib',
            field=models.IntegerField(default=0, verbose_name='id flibusta'),
        ),
        migrations.AlterField(
            model_name='news',
            name='views',
            field=models.IntegerField(verbose_name='Просмотры'),
        ),
    ]