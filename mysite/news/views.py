from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.db.models import F, Count
import collections

from .models import News, Category, Author, Series
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import os

import lxml.html
from lxml import etree
from math import ceil


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


class SearchResultsView(ListView):
    model = News
    template_name = "news/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is None:
            return News.objects.filter(pk=0)
        return News.objects.filter(title__icontains=query)

        # else:
        #     object_list = News.objects.filter(
        #         Q(title__icontains=query) | Q(author__icontains=query)
        #     )
        #     return object_list


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Читать книги онлайн полностью бесплатно и без регистрации'
        context['description'] = 'Litgroup.info - библиотека бесплатных онлайн книг, которые можно читать онлайн'
        context['mixin_prop'] = self.get_prop()
        context['cnt'] = News.objects.filter(is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'Список новостей'
#     }
#     return render(request, 'news/index.html', context)


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['cnt'] = News.objects.filter(category__slug=self.kwargs['slug'], is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'], is_published=True)
        # return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    @property
    def items_count(self):
        # получаем список идентификторов всех низлежащих категорий, включая интересующую нас
        # ids = self.get_descendants(include_self=True).values_list('id')
        # возвращаем количество товаров, имеющих родителем категорию с идентификатором входящим
        # в список полученный строкой выше
        # catigouris = News.objects.annotate(items_count=Count('related_name_to_items'))
        cats = News.objects.annotate(cnt=Count('news', filter=F('news__is_published')))
        return cats


class NewsByAuthor(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Author.objects.get(slug=self.kwargs['slug'])
        context['cnt'] = News.objects.filter(author__slug=self.kwargs['slug'], is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(author__slug=self.kwargs['slug'], is_published=True)


class NewsBySeries(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Series.objects.get(slug=self.kwargs['slug'])
        context['cnt'] = News.objects.filter(series__slug=self.kwargs['slug'], is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(series__slug=self.kwargs['slug'], is_published=True)




class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.series:
            context['ser'] = News.objects.filter(series__pk=self.object.series.pk)
            # context['sers'] = sorted([i.series_num for i in context['ser'] if type(i.series_num) == int])
            context['sers'] = {i.series_num: [i.title, i.slug] for i in context['ser'] if type(i.series_num) == int}
            context['sers'] = collections.OrderedDict(sorted(context['sers'].items()))
        if "viewss" not in self.request.session:
            self.request.session["viewss"] = ''

        if str(self.object.pk) in self.request.session['viewss'].split(','):
            self.request.session["viewss"] = self.request.session["viewss"].replace(str(self.object.pk) + ',', '')
            self.request.session['viewss'] = self.request.session['viewss'] + str(str(self.object.pk) + ',')

        if str(self.object.pk) not in self.request.session['viewss'].split(','):
            self.request.session['viewss'] = self.request.session['viewss'] + str(str(self.object.pk) + ',')
            self.object.views = F('views') + 1
            self.object.save(viewss='views')
            self.object.refresh_from_db()

        # self.request.session["viewss"] = ''

        return context


# class CreateNews(LoginRequiredMixin, CreateView):
#     form_class = NewsForm
#     template_name = 'news/add_news.html'
#     login_url = '/admin/'
#     permission_denied_message = 'You need to log in'
#     success_url = reverse_lazy('home')
#     raise_exception = True


@login_required(login_url="login")
def profile(request):
    return render(request, 'news/profile.html')


def genres(request):
    cnt = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published')))
    return render(request, 'news/genres.html', {'cnt': cnt})


def authors(request):
    cnt = Author.objects.annotate(cnt=Count('news', filter=F('news__is_published')))
    return render(request, 'news/authors.html', {'cnt': cnt})


def series(request):
    cnt = Series.objects.annotate(cnt=Count('news', filter=F('news__is_published')))
    return render(request, 'news/series.html', {'cnt': cnt})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'djangoalex@ukr.net',
                             ['saddon11@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка отправки')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})


def read(request, book_id, book_page):
    news_item = News.objects.get(pk=book_id)
    xslt_doc = etree.parse("test.xsl")

    try:
        xslt_transformer = etree.XSLT(xslt_doc)
        source_doc = etree.parse(news_item.fb2)
    except:
        return render(request, 'news/read_book.html', {'news_item': news_item, 'readp': 'read', 'error': 'Ошибка'})

    output_doc = xslt_transformer(source_doc)

    if 'ul' in str(output_doc):
        nav1 = str(output_doc).split('<ul>')
        nav1 = str(nav1[1]).split('</ul>')
    else:
        nav1 = ['']

    output_doc = str(output_doc).split('<p>')
    p = 25
    pages = ceil(len(output_doc) / p)

    output_doc = output_doc[int(p * (book_page - 1)):int((p * (book_page - 1)) + p)]

    listpages = [int(i) for i in range(1, pages + 1)]
    page = request.GET.get('page')
    if page:
        return redirect('read', book_id=book_id, book_page=page)
    else:
        return render(request, 'news/read_book.html',
                      {'news_item': news_item, 'values': output_doc, 'pages': pages, 'page': book_page,
                       'listpages': listpages, 'nav': nav1[0], 'readp': 'read'})




def parse(request):
    mytree = ET.parse('gp1.fb2')
    myroot = mytree.getroot()

    return render(request, 'parse.html', {'values': myroot})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /read/",
        "Disallow: /*?*",
        "Sitemap: https://bookread.com.ua/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class SitemapXmlView(TemplateView):
    template_name = 'sitemapxml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = News.objects.all().order_by('-created_at')
        return context

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'news/category.html', context)
