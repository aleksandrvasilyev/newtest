# Generated by Django 3.2.13 on 2022-08-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Url'),
        ),
    ]
