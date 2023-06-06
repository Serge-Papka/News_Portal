from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin


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


@login_required
@permission_required('News_Portal.add_post', raise_exception=True)
def create_news(request):  # способ 1
    is_not_author = not request.user.groups.filter(name='authors').exists()
    if request.method == 'POST':
        form3 = PostForm(request.POST)
        if form3.is_valid():
            form3.save()
            post_c = form3.save(commit=False)
            post_c.position = 'NE'  # задаем значение поля position
            post_c.save()
            return HttpResponseRedirect(reverse('NewsDetail2', args=[post_c.pk]))
        else:
            return render(request, 'news_create.html', {'form': form3,
                                                        'is_not_author': is_not_author})
    form2 = PostForm()
    return render(request, 'news_create.html', {'form': form2,
                                                'is_not_author': is_not_author})


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):  # способ 2 Джинерик
    permission_required = 'News_Portal.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post_ = form.save(commit=False)
        post_.position = 'AR'
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'News_Portal.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'AR':
            raise Http404("This not news")
        user = self.request.user
        print(user, 999111)
        if not user.is_authenticated:
            print("You must be logged in to edit news")
        return obj

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'News_Portal.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    pk_url_kwarg = 'p_keyArticleUpdate'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.position == 'NE':
            raise Http404("This not a article")
        return obj

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


# Представление удаляющее товар.
class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'News_Portal.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news-list')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'News_Portal.delete_post'
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect(request.META['HTTP_REFERER'])


def downgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        premium_group.user_set.remove(user)
    return redirect('/')

# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('<app>.<action>_<model>',
#                            '<app>.<action>_<model>')
