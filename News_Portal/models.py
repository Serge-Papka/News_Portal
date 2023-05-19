from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь «один к одному»
    # с встроенной моделью пользователей User;
    author_name = models.CharField(max_length=30, blank=True)  # тест
    ratio = models.IntegerField(default=0)  # Рейтинг пользователя. Ниже дано как этот рейтинг можно посчитать.

    # def save(self, *args, **kwargs):
    #     if not self.author_name:
    #         self.author_name = models.
    #     super().save(*args, **kwargs)

    def update_rating(self):  # Обновляет рейтинг текущего автора
        ratio_posts_autor = Post.objects.filter(author_id=self.pk).aggregate(ratio_pa=Sum('ratio'))['ratio_pa']
        ratio_comments_autor = Comment.objects.filter(user_id=self.user).aggregate(ratio_ca=Sum('ratio'))['ratio_ca']
        ratio_users_comments = Comment.objects.filter(post__author__user=self.user).aggregate(ratio_uc=Sum('ratio'))[
            'ratio_uc']
        self.ratio = ratio_posts_autor * 3 + ratio_comments_autor + ratio_users_comments
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # OK


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author;
    position = models.CharField(max_length=2, choices=POSITIONS, default=article)  # «статья» или «новость»;
    date_time = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания;
    category = models.ManyToManyField('Category', through='PostCategory')  # связь «многие ко многим»
    #                                           с моделью Category (с дополнительной моделью PostCategory);
    title = models.CharField(max_length=50)  # заголовок статьи/новости;
    text = models.TextField(default="Текст отсутствует.")  # текст статьи/новости;
    ratio = models.IntegerField(default=0)  # рейтинг статьи/новости."

    def like(self):
        self.ratio += 1
        self.save()

    def dislike(self):
        self.ratio -= 1
        self.save()

    def preview(self):  # Возвращает начало статьи (предварительный просмотр) длиной 124 символа
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category.


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # связь «один ко многим» со встроенной моделью User
    # (комментарии может оставить любой пользователь,
    # необязательно автор);
    text = models.TextField()  # текст комментария;
    date_time = models.DateTimeField(auto_now_add=True)  # дата и время создания комментария;
    ratio = models.IntegerField(default=0)  # рейтинг комментария.

    def like(self):
        self.ratio += 1
        self.save()

    def dislike(self):
        self.ratio -= 1
        self.save()
