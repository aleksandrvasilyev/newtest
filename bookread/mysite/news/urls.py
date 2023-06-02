from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('robots.txt', robots_txt),
    path('contact/', contact, name='contact'),
    path('genres/', genres, name='genres'),
    path('series/', series, name='series'),
    path('authors/', authors, name='authors'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('read/<int:book_id>/<int:book_page>', read, name='read'),
    path('parse/', parse, name='parse'),
    path('profile/', profile, name='profile'),
    # path('', index, name='home'),
    # path('', cache_page(60) (HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('genre/<str:slug>/', NewsByCategory.as_view(), name='category'),
    #path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('author/<str:slug>/', NewsByAuthor.as_view(), name='author'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('serie/<str:slug>/', NewsBySeries.as_view(), name='series'),
    path('<str:slug>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    # path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('sitemap.xml', SitemapXmlView.as_view()),

]

# appname='news'