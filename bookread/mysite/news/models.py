from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from unidecode import unidecode
from django.template import defaultfilters


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    #     author = models.CharField(max_length=150, default='', blank=True, verbose_name='Автор')
    author = models.ForeignKey('Author', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Автор')
    series = models.ForeignKey('Series', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Серия')
    content = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение', blank=True, default='image/book.png')
    fb2 = models.FileField(upload_to='books/%Y/%m/%d/', verbose_name='fb2 файл', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Категория')
    views = models.IntegerField(default=0)
    series_num = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=50, verbose_name='ISBN', null=True, blank=True)
    year = models.CharField(max_length=10, verbose_name='year', null=True, blank=True)
    idflib = models.IntegerField(verbose_name='id flibusta', null=True)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def save(self, *args, viewss=0, **kwargs):
        if viewss == 'views':
            super(News, self).save(*args, **kwargs)
        else:
            sl = unidecode(str(self.title))
            # self.slug = slugify(sl)

            i = 2
            slug1 = slugify(sl)
            while News.objects.filter(slug=slug1).exists():
                # self.slug = slugify(sl) + '-' + str(i)
                slug1 = slugify(sl) + '-' + str(i)
                i += 1
            self.slug = slug1
            super(News, self).save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    id_flib = models.IntegerField(default=0)

    def get_absolute_url(self):
        # return reverse('category', kwargs={'category_id': self.pk})
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def save(self, *args, **kwargs):
        sl = unidecode(str(self.title))
        self.slug = slugify(sl)
        super(Category, self).save(*args, **kwargs)


class Author(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Автор')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    # slug = models.SlugField(unique=True)
    id_flib = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('author', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['title']

    def save(self, *args, **kwargs):
        sl = unidecode(str(self.title))
        self.slug = slugify(sl)
        super(Author, self).save(*args, **kwargs)


class Series(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Серия')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    id_flib = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('series', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        ordering = ['title']

    def save(self, *args, **kwargs):
        sl = unidecode(str(self.title))
        self.slug = slugify(sl)
        super(Series, self).save(*args, **kwargs)
