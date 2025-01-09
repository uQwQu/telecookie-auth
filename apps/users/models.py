import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomUserManager


class User(AbstractUser):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=60,
        unique=True,
    )
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
