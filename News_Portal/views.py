from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    # model = Post
    # ordering = 'title'
    queryset = Post.objects.filter(position='NE').order_by('-date_time')
    template_name = 'news.html'
    context_object_name = 'news_list'


class ArticleList(ListView):
    # model = Post
    # ordering = 'title'
    queryset = Post.objects.filter(position='AR').order_by('-date_time')
    template_name = 'article.html'
    context_object_name = 'article_list'


class NewsDetail(DetailView):
    model = Post
    template_name = 'a_single_news.html'
    context_object_name = 'news_solo'
    pk_url_kwarg = 'p_key'
