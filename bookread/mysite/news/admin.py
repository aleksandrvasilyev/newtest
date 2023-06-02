from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.utils.text import slugify

from . import models
from .models import News, Category, Author, Series
from import_export.admin import ImportExportModelAdmin
from django.db.models import QuerySet


class ForeignKeyWidgetWithCreation(ForeignKeyWidget):
    """
    Taken from a GitHub post.
    https://github.com/django-import-export/django-import-export/issues/318#issuecomment-139989178
    """

    def __init__(self, model, field="pk", create=False, **kwargs):
        self.model = model
        self.field = field
        self.create = create
        super(ForeignKeyWidgetWithCreation, self).__init__(model, field=field, **kwargs)

    def clean(self, value, **kwargs):
        if not value:
            return None

        if self.create:
            self.model.objects.get_or_create(**{self.field: value})

        val = super(ForeignKeyWidgetWithCreation, self).clean(value, **kwargs)

        return self.model.objects.get(**{self.field: val}) if val else None


class NewsResource(resources.ModelResource):
    author = fields.Field(attribute='author',
                          widget=ForeignKeyWidgetWithCreation(model=models.Author, field='title', create=True))
    series = fields.Field(attribute='series',
                          widget=ForeignKeyWidgetWithCreation(model=models.Series, field='title', create=True))
    category = fields.Field(attribute='category',
                            widget=ForeignKeyWidgetWithCreation(model=models.Category, field='title', create=True))

    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'author', 'series', 'content', 'created_at', 'updated_at', 'photo', 'fb2',
                  'is_published', 'category', 'views', 'series_num', 'isbn', 'year', 'idflib')
        import_id_fields = ('idflib',)

    def skip_row(self, instance, original):
        if not original.idflib:
            return False
        return True
        # return getattr(original, "idflib") == getattr(instance, "idflib")


        # if original_id_value == instance_id_value:
        #     return True
        # return instance.idflib == original.idflib
        # if not original.idflib:
        #     return False
        # return True

    def after_import_row(self, row, row_result, row_number=None, aut=author, **kwargs):
        pass
        # Author.objects.filter(title=row['author']).update(**{'slug': slugify(row['author'], allow_unicode=True), 'id_flib': 1})
        # try:
        #     # Author.objects.get_or_create(title=self.author, slug='abcdef')
        #     # Author.objects.get_or_create(title='Артур Конан Дойль да нет 2 ест', slug='abcdef')
        #     # Author.objects.filter(title='Тест4').get_or_update(slug='test4')
        #
        #
        #     # Author.objects.filter(title='Тест5').update(**{'slug': 'test5-ya-dadaya'})
        #
        #     # Author.objects.filter(title=str(self.author)).update(**{'slug': 'test5-ya-dadaya'})
        #     Author.objects.filter(title='Тест5').update(**{'slug': 'test5-ya-dadaya2', 'id_flib': row_result})
        #
        #
        # except Exception as e:
        #     print(e)
        # return row


# class NewsAdmin(admin.ModelAdmin):
class NewsAdmin(ImportExportModelAdmin):
    resource_class = NewsResource
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ['title']
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'slug', 'author', 'category', 'series', 'series_num', 'content', 'photo', 'fb2', 'isbn', 'year',
              'idflib', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('updated_at', 'created_at', 'get_photo', 'views')
    save_on_top = True


    @admin.display(
        description='Миниатюра',
    )
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title')
    list_display_links = ['id', 'title']
    search_fields = ('title',)


class AuthorAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ['id', 'title']
    search_fields = ('title',)
    fields = ('title', 'slug', 'id_flib')


class SeriesAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ['id', 'title']
    search_fields = ('title',)
    fields = ('title', 'slug', 'id_flib')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Series, SeriesAdmin)
