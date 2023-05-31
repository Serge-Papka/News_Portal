from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Post


# Добавьте страницу /news/search. На ней должна быть реализована возможность искать
# новости по определённым критериям. Критерии должны быть следующие:
# по названию
# по имени автора
# позже указываемой даты
# Убедитесь, что можно выполнить фильтрацию сразу по нескольким критериям.

class NewsList(ListView):
    # model = Post
    # ordering = 'title'
    queryset = Post.objects.filter(position='NE').order_by('-date_time')
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10  # вот так мы можем указать количество записей на странице


class SearchNe(ListView):
    queryset = Post.objects.filter(position='NE').order_by('-date_time')
    template_name = 'search.html'
    context_object_name = 'news_list'
    paginate_by = 5

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    # model = Post
    # ordering = 'title'
    queryset = Post.objects.filter(position='AR').order_by('-date_time')
    template_name = 'article.html'
    context_object_name = 'article_list'
    paginate_by = 3


class NewsDetail(DetailView):
    model = Post
    template_name = 'a_single_news.html'
    context_object_name = 'news_solo'
    pk_url_kwarg = 'p_key'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'AR':
            raise Http404("This not news")
        return obj


class ArticleDetail(DetailView):
    model = Post
    template_name = 'a_single_news.html'
    context_object_name = 'news_solo'
    pk_url_kwarg = 'p_key'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'NE':
            raise Http404("This not a article")
        return obj


def create_news(request):  # способ 1
    if request.method == 'POST':
        form3 = PostForm(request.POST)
        if form3.is_valid():
            form3.save()
            post_c = form3.save(commit=False)
            post_c.position = 'NE'  # задаем значение поля position
            post_c.save()
            return HttpResponseRedirect(reverse('NewsDetail2', args=[post_c.pk]))
        else:
            return render(request, 'news_create.html', {'form': form3})
    form2 = PostForm()
    return render(request, 'news_create.html', {'form': form2})  # , 'position': 'NE'})


class PostCreate(CreateView):  # способ 2 Джинерик
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post_ = form.save(commit=False)
        post_.position = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'AR':
            raise Http404("This not news")
        return obj


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    pk_url_kwarg = 'p_keyArticleUpdate'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'NE':
            raise Http404("This not a article")
        return obj


# Представление удаляющее товар.
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news-list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')