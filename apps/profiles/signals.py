from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import Profile
from config.settings import AUTH_USER_MODEL


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:
    if created:
        Profile.objects.create(user=instance)
