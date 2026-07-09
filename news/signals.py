from allauth.account.signals import user_signed_up
from .models import Post
from .tasks import send_notification, send_welcome_email
from datetime import datetime
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    """Сброс кэша при изменении статьи"""
    # Сбрасываем кэш для конкретной статьи
    cache.delete(f'post_cache_{instance.pk}_{instance.rating}')
    # Сбрасываем кэш страницы со списком
    cache.clear()  # или более точечно


@receiver(user_signed_up)
def welcome_email_signal(request, user, **kwargs):
    """Отправляем приветственное письмо через Celery"""
    send_welcome_email.delay(user.email, user.username)


@receiver(post_save, sender=Post)
def notify_subscribers_signal(sender, instance, created, **kwargs):
    """Уведомляем подписчиков через Celery"""
    if created and instance.post_type == 'news':
        categories = instance.categories.all()

        for category in categories:
            for user in category.subscribers.all():
                send_notification.delay(
                    instance.pk,
                    category.pk,
                    user.email,
                    user.username
                )


@receiver(post_save, sender=Post)
def check_post_limit(sender, instance, created, **kwargs):
    """Проверка лимита постов"""
    if created:
        today = datetime.now().date()
        author = instance.author
        posts_today = Post.objects.filter(
            author=author,
            created_at__date=today
        ).count()

        if posts_today > 3:
            instance.delete()
            raise ValueError('Нельзя публиковать более 3 новостей в сутки!')