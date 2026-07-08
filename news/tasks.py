from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from datetime import datetime, timedelta


@shared_task
def send_notification(post_id, category_id, user_email, username):
    """Отправка уведомления подписчику"""
    post = Post.objects.get(pk=post_id)
    category = Category.objects.get(pk=category_id)

    subject = post.title
    html_content = render_to_string('email/new_post.html', {
        'user': {'username': username},
        'post': post,
        'category': category
    })

    msg = EmailMultiAlternatives(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    return f'Email sent to {username}'


@shared_task
def send_welcome_email(user_email, username):
    """Приветственное письмо"""
    subject = 'Добро пожаловать в NewsPortal!'
    html_content = render_to_string('email/welcome.html', {
        'user': {'username': username}
    })

    msg = EmailMultiAlternatives(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_newsletter():
    """Еженедельная рассылка"""
    week_ago = datetime.now() - timedelta(days=7)

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category,
            post_type='news',
            created_at__gte=week_ago
        )

        if new_posts.exists():
            for user in category.subscribers.all():
                html_content = render_to_string('email/weekly.html', {
                    'user': user,
                    'category': category,
                    'posts': new_posts
                })

                msg = EmailMultiAlternatives(
                    f'Новые статьи в категории {category.name}',
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

    return 'Weekly newsletter sent'