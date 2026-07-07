from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Category
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Отправка еженедельной рассылки'

    def handle(self, *args, **options):
        week_ago = datetime.now() - timedelta(days=7)

        for category in Category.objects.all():
            new_posts = category.post_set.filter(
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