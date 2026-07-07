from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group, User
from .models import Post, Category
from datetime import datetime, timedelta


# Приветственное письмо при регистрации
@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    subject = 'Добро пожаловать в NewsPortal!'
    html_content = render_to_string('email/welcome.html', {'user': user})
    msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Письмо подписчикам при создании новости
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == 'news':
        categories = instance.categories.all()
        subscribers = set()

        for category in categories:
            subscribers.update(category.subscribers.all())

        for user in subscribers:
            subject = instance.title
            html_content = render_to_string('email/new_post.html', {
                'user': user,
                'post': instance,
                'category': category
            })
            msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


# Проверка на 3 поста в сутки (через сигнал)
@receiver(post_save, sender=Post)
def check_post_limit(sender, instance, created, **kwargs):
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

@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    group, created = Group.objects.get_or_create(name='common')
    user.groups.add(group)