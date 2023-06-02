from django import template
from django.db.models import Count, F, Case, When
from news.models import News, Category, Author, Series

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    # return Category.objects.all()
    return Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)


@register.simple_tag(name='get_list_authors')
def get_authors():
    # return Category.objects.all()
    return Author.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)


@register.simple_tag(name='get_list_series')
def get_series():
    # return Category.objects.all()
    return Series.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=5)
    return {"categories": categories}


@register.inclusion_tag('news/list_popular.html')
def show_popular(cnt=5):
    posts = News.objects.order_by('-views')[:cnt]
    return {"posts": posts}


@register.inclusion_tag('news/slider_viewed.html', takes_context=True)
# @register.simple_tag(takes_context=True, name='list_view')
def get_views(context, **kwargs):
    if "viewss" not in context.request.session:
        context.request.session["viewss"] = ''

    book_list = list(filter(None, context.request.session['viewss'].split(',')))
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(book_list)])
    posts = News.objects.filter(pk__in=book_list).order_by(preserved).reverse()[:5]
    return {"posts": posts}
