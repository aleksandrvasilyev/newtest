# Generated by Django 3.2.13 on 2022-08-03 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
