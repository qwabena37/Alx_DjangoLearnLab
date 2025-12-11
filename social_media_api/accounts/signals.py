from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import User
from notifications.utils import create_notification

@receiver(m2m_changed, sender=User.followers.through)
def followers_changed(sender, instance, action, reverse, pk_set, **kwargs):
    """
    When someone follows (adds to instance.followers), we create a notification.
    `instance` is the User whose followers set changed.
    `pk_set` are ids of users added/removed.
    """
    if action == 'post_add':
        # pk_set are follower ids
        for follower_id in pk_set:
            try:
                follower = User.objects.get(pk=follower_id)
            except User.DoesNotExist:
                continue
            # actor is follower, recipient is the instance (user being followed)
            create_notification(recipient=instance, actor=follower, verb='followed', target=instance)
