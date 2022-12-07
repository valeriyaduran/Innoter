import json

from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver

from innoapp.models import Post, Page
from innoapp.producer import SendStatisticsClient


@receiver(post_save, sender=Page)
def send_pages_count_to_microservice(sender, instance, **kwargs):
    if kwargs['created']:
        body = {
                'action': 'page_added',
            }
        producer = SendStatisticsClient()
        producer.send_statistics(body=json.dumps(body))


@receiver(post_save, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    if kwargs['created']:
        body = {
                'action': 'post_added',
            }
        producer = SendStatisticsClient()
        producer.send_statistics(body=json.dumps(body))


@receiver(post_delete, sender=Post)
def send_posts_count_to_microservice(sender, instance, **kwargs):
    body = {
        'action': 'post_deleted',
    }
    producer = SendStatisticsClient()
    producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Post.liked_by.through)
def send_likes_count_to_microservice(instance, action, pk_set, **kwargs):
    producer = SendStatisticsClient()
    if action == 'post_add':
        body = {
            'action': 'like_added',
        }
        producer.send_statistics(body=json.dumps(body))
    if action == 'post_remove':
        body = {
            'action': 'like_removed',
        }
        producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Page.follow_requests.through)
def send_follow_requests_count_to_microservice(instance, action, pk_set, **kwargs):
    producer = SendStatisticsClient()
    if action == "post_add" and pk_set:
        body = {
            'action': 'follow_request_added',
        }
        producer.send_statistics(body=json.dumps(body))
    if action == "post_remove" and pk_set:
        body = {
            'action': 'follow_request_removed',
        }
        producer.send_statistics(body=json.dumps(body))


@receiver(m2m_changed, sender=Page.followers.through)
def send_followers_count_to_microservice(instance, action, pk_set, **kwargs):
    producer = SendStatisticsClient()
    if action == "post_add" and pk_set:
        body = {
            'action': 'follower_added',
        }
        producer.send_statistics(body=json.dumps(body))




