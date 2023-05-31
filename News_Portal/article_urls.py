from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail, ArticleList, SearchNe, PostCreate, ArticleDetail, ArticleUpdate, ArticleDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # path('', NewsList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:p_key>', ArticleDetail.as_view(), name='arst'),
   path('', ArticleList.as_view(), name='article_list'),
   # path('search/',  SearchNe.as_view()),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:p_keyArticleUpdate>/update/', ArticleUpdate.as_view(), name='articleUpdate'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_del'),
]