# Generated by Django 4.2.1 on 2023-06-01 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0041_auto_20220912_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, default='image/book.png', upload_to='photos/%Y/%m/%d/', verbose_name='Изображение'),
        ),
    ]