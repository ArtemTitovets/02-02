from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.cache import cache
from django.urls import reverse



class Author(models.Model):   # Модель автор
    rating = models.IntegerField(default=0.0)   # рейтинг пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # cвязь «один к одному» с встроенной моделью пользователей User

    def update_rating(self):
        author_post_rating = self.posts.aggregate(post_rating_sum=Coalesce(Sum('rating'), 0)).get("post_rating_sum")
        author_comment_rating = self.user.comments.aggregate(commets_rating_sum=Coalesce(Sum('rating'), 0)).get("commets_rating_sum")
        author_post_comment_rating = self.posts.aggregate(commets_rating_sum=Coalesce(Sum('rating'), 0)).get("commets_rating_sum")
        self.rating = author_post_rating * 3 + author_comment_rating + author_post_comment_rating
        self.save()


class Category(models.Model):   # Модель Category

    sport = "SP"
    politics = "PO"
    health = "HE"
    cars = "CA"

    CATEGORY = [(sport, "спорт"),
                (politics, "политика"),
                (health, "здоровье"),
                (cars, "автомобили"),]

    category = models.CharField(max_length=2, choices=CATEGORY, unique=True)   # название категории
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', verbose_name='Подписчики')

    def __str__(self):
        return self.category


class Post(models.Model):   # Модель Post

    article = 'AR'
    news = 'NE'

    POSITIONS = [(article, 'Статья'),
                 (news, 'Новость'),]

    post = models.CharField(max_length=2, choices=POSITIONS, default=article)   # поле с выбором — «статья» или «новость»
    time_in = models.DateTimeField(auto_now_add=True)   # автоматически добавляемая дата и время создания
    heading = models.CharField(max_length=64, verbose_name='Заголовок')   # заголовок статьи/новости
    text = models.TextField(verbose_name='Содержание')   # текст статьи/новости
    rating = models.IntegerField(default=0.0)   # рейтинг статьи/новости
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')   # связь «один ко многим» с моделью Author
    category = models.ManyToManyField(Category, "PostCategory")  # связь «многие ко многим» с моделью Category

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        view = self.text[0:125] + "..."
        return view

    def __str__(self):
        return f'{self.heading.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        # return reverse('news_detail', args=[str(self.id)])
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):   # Промежуточная модель для связи «многие ко многим»
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   # связь «один ко многим» с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)   # связь «один ко многим» с моделью Category


class Comment(models.Model):   # Модель Comment
    text_comment = models.CharField(max_length=255)   # текст комментария
    time_in_comment = models.DateTimeField(auto_now_add=True)   # дата и время создания комментария
    rating = models.IntegerField(default=0.0)   # рейтинг комментария
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   # cвязь «один ко многим» с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # 	связь «один ко многим» со встроенной моделью User

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
