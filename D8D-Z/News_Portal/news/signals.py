# from django.template.loader import render_to_string
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from .models import Post
#
#
# def send_notifications(preview, pk, heading, subscribers):
#     html_content = render_to_string(
#                                     'post_created_email.html',
#                                     {'text': preview,
#                                             'link': f'{settings.SITE_URL}/news/{pk}'}
#                                    )
#
#     msg = EmailMultiAlternatives(subject=heading,
#                                  body='',
#                                  from_email=settings.EMAIL_HOST_USER + '@yandex.ru',
#                                  to=subscribers,
#                                 )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=Post.category.through)
# def notification_of_news_creation(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers_notification = []
#
#         for c in categories:
#             subscribers = c.subscribers.all()
#             subscribers_notification += [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.heading, subscribers_notification)
