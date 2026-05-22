from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection

from common.models import UserProfile
from common.utils.helpers import USER_MODEL


@receiver(post_save, sender=USER_MODEL)
def user_creation_handler(sender, instance, created, **kwargs):
    if created:
        if connection.schema_name == 'public':
            return  # Stop here! Don't create profiles for God Users
        co_workers, created = Group.objects.get_or_create(name='co-workers')
        instance.groups.add(co_workers)
        UserProfile.objects.create(user=instance)
