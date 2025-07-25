from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)