from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile

User = get_user_model()


class TgAccount(models.Model):
    profile = models.OneToOneField(
        Profile, related_name="tg", on_delete=models.CASCADE, null=True, blank=True
    )
    temporary_token = models.CharField(
        max_length=50, unique=True, null=True, blank=True
    )
    temporary_token_expiration = models.DateTimeField(null=True, blank=True)
    telegram_id = models.BigIntegerField(
        unique=True, editable=False, null=True, blank=True
    )
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Telegram Account")
        verbose_name_plural = _("Telegram Accounts")

    def __str__(self):
        return self.first_name
