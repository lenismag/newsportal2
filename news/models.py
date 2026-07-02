from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    """Модель автора, связана с пользователем один-к-одному."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """Обновляет рейтинг автора по формуле:
        сумма рейтингов всех постов автора * 3
        + сумма рейтингов всех комментариев автора
        + сумма рейтингов всех комментариев к постам автора.
        """
        # Все посты автора
        posts = Post.objects.filter(author=self)
        post_rating = sum(p.rating for p in posts) * 3

        # Все комментарии, написанные этим пользователем (автором)
        comments_author = Comment.objects.filter(user=self.user)
        comment_rating_author = sum(c.rating for c in comments_author)

        # Все комментарии к постам автора (не важно, кто их написал)
        comments_to_posts = Comment.objects.filter(post__author=self)
        comment_rating_to_posts = sum(c.rating for c in comments_to_posts)

        self.rating = post_rating + comment_rating_author + comment_rating_to_posts
        self.save()

class Category(models.Model):
    """Категория новостей/статей. Название уникально."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'

    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        """Возвращает первые 124 символа текста и добавляет многоточие, если текст длиннее."""
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text

class PostCategory(models.Model):
    """Промежуточная модель для связи ManyToMany между Post и Category."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    """Комментарий к посту."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()