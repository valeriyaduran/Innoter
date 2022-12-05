import json

from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from innoapp.models import Post, Page
from innoapp.producer import SendStatisticsClient
from innoapp.services.statistics_storage import StatisticsStorage


@receiver(post_save, sender=Page)
def send_pages_count_to_microservice(sender, instance, **kwargs):
    data = StatisticsStorage.get_pages_count_data(instance.pk)
    body = {
            'action': 'page_add',
            'pages_count': len(data)
        }
    print("pages after save", len(data))
    producer = SendStatisticsClient()
    producer.send_statistics(body=json.dumps(body))


@receiver(post_save, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    data = StatisticsStorage.get_posts_count_data(instance.pk, 'post_save')
    body = {
        'action': 'post_add',
        'posts_count': len(data)
    }
    print("posts after save", len(data))
    producer = SendStatisticsClient()
    producer.send_statistics(body=json.dumps(body))


@receiver(post_delete, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    data = StatisticsStorage.get_posts_count_data(instance.pk, 'post_delete')
    body = {
        'action': 'post_delete',
        'posts_count': len(data)
    }
    print("posts after delete", len(data))
    producer = SendStatisticsClient()
    producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Post.liked_by.through)
def send_likes_count_to_microservice(instance, action, pk_set, **kwargs):
    if action == "post_add":
        likes_count = 0
        for post in Post.objects.all():
            likes_count += post.liked_by.all().count()


@receiver(m2m_changed, sender=Page.followers.through)
def send_followers_count_to_microservice(instance, action, pk_set, **kwargs):
    if action == "post_add":
        followers_count = 0
        for page in Page.objects.all():
            followers_count += page.followers.all().count()


@receiver(m2m_changed, sender=Page.follow_requests.through)
def send_follow_requests_count_to_microservice(instance, action, pk_set, **kwargs):
    if action == "post_add":
        follow_requests_count = 0
        for page in Page.objects.all():
            follow_requests_count += page.follow_requests.all().count()
