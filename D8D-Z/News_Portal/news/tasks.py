from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
import datetime


@shared_task
def add_new_post_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    heading = post.heading
    subscribers_emails = []
    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string('post_created_email.html',
                                    {'text': f'{post.heading[0:50]}',
                                            'link': f'{settings.SITE_URL}/news/{pk}'}
                                   )
    msg = EmailMultiAlternatives(subject=heading,
                                 body='',
                                 from_email=settings.EMAIL_HOST_USER + '@yandex.ru',
                                 to=subscribers_emails,)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def sending_emails_every_week_task():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)
    posts_7_day = Post.objects.filter(time_in__gte=last_week)

    for cat in Category.objects.all():
        post_list = posts_7_day.filter(category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string('daily_post.html',
                                            {'link': settings.SITE_URL,
                                            'posts': post_list,}
                                            )
            msg = EmailMultiAlternatives(subject=f'Новые посты за прошедшую неделю в категории {cat.category}',
                                         body='',
                                         from_email=settings.EMAIL_HOST_USER + '@yandex.ru',
                                         to=recipients, )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()