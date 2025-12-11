from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from notifications.utils import create_notification
from .models import Comment

@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.user
        recipient = post.author
        create_notification(recipient=recipient, actor=actor, verb='liked', target=post)


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        actor = instance.author
        recipient = post.author
        create_notification(recipient=recipient, actor=actor, verb='commented', target=instance)