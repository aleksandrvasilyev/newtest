# Generated by Django 3.2.13 on 2022-08-01 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20220628_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.CharField(default=None, max_length=150, verbose_name='Автор'),
        ),
    ]
