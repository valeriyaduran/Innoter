import json

from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from innoapp.models import Post, Page
from innoapp.producer import SendStatisticsClient
from innoapp.serializers import PageSerializer, PostSerializer


@receiver(post_save, sender=Page)
def send_pages_count_to_microservice(sender, instance, **kwargs):
    serializer = PageSerializer(data=instance)
    if kwargs['created']:
        body = {
            'user_id': serializer.initial_data.owner.pk,
            'action': 'page_added',
        }
        producer = SendStatisticsClient()
        producer.send_statistics(body=json.dumps(body))


@receiver(post_save, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    serializer = PostSerializer(data=instance)
    if kwargs['created']:
        body = {
            'user_id': serializer.initial_data.page.owner.pk,
            'action': 'post_added',
        }
        producer = SendStatisticsClient()
        producer.send_statistics(body=json.dumps(body))


@receiver(post_delete, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    serializer = PostSerializer(data=instance)
    body = {
        'user_id': serializer.initial_data.page.owner.pk,
        'action': 'post_deleted',
    }
    producer = SendStatisticsClient()
    producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Post.liked_by.through)
def send_likes_count_to_microservice(instance, action, pk_set, **kwargs):
    serializer = PostSerializer(data=instance)
    producer = SendStatisticsClient()
    if action == 'post_add':
        body = {
            'user_id': serializer.initial_data.page.owner.pk,
            'action': 'like_added',
        }
        producer.send_statistics(body=json.dumps(body))
    if action == 'post_remove':
        body = {
            'user_id': serializer.initial_data.page.owner.pk,
            'action': 'like_removed',
        }
        producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Page.follow_requests.through)
def send_follow_requests_count_to_microservice(instance, action, pk_set, **kwargs):
    serializer = PageSerializer(data=instance)
    producer = SendStatisticsClient()
    if action == "post_add" and pk_set:
        body = {
            'user_id': serializer.initial_data.owner.pk,
            'action': 'follow_request_added',
        }
        producer.send_statistics(body=json.dumps(body))
    if action == "post_remove" and pk_set:
        body = {
            'user_id': serializer.initial_data.owner.pk,
            'action': 'follow_request_removed',
        }
        producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Page.followers.through)
def send_followers_count_to_microservice(instance, action, pk_set, **kwargs):
    serializer = PageSerializer(data=instance)
    producer = SendStatisticsClient()
    if action == "post_add" and pk_set:
        body = {
            'user_id': serializer.initial_data.owner.pk,
            'action': 'follower_added',
        }
        producer.send_statistics(body=json.dumps(body))

