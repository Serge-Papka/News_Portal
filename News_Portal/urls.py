from django.urls import path
# Импортируем созданные нами представления
from .views import NewsList, NewsDetail, ArticleList, SearchNe, create_news, NewsUpdate, NewsDelete

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', NewsList.as_view(), name='news-list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:p_key>', NewsDetail.as_view(), name='NewsDetail2'),
    # path('article/', ArticleList.as_view()),
    path('search/', SearchNe.as_view()),
    path('create/', create_news, name='news_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_up'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_del'),
]
