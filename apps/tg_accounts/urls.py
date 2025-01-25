from django.urls import path

from apps.tg_accounts.bot.services import activate_session
from apps.tg_accounts.bot.webhook import telegram_webhook

from . import views

urlpatterns = [
    path(
        "session/<str:temporary_token>/",
        activate_session,
        name="activate_session",
    ),
    path("webhook/", telegram_webhook, name="telegram_webhook"),
    path("linking/", views.telegram_linking, name="telegram_linking"),
    path("auth/", views.telegram_auth, name="telegram_auth"),
]
