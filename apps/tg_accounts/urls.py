from django.urls import path

from apps.tg_accounts.services import activate_session

from . import views
from .webhook import telegram_webhook

urlpatterns = [
    path(
        "activate-session/<str:temporary_token>/",
        activate_session,
        name="activate_session",
    ),
    path("webhook/", telegram_webhook, name="telegram_webhook"),
    path("linking/", views.telegram_linking, name="telegram_linking"),
    path("signup/", views.telegram_signup, name="telegram_signup"),
    path("logout/", views.logout, name="logout"),
]
