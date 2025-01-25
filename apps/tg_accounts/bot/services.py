import secrets
from datetime import timedelta

from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now

from apps.tg_accounts.models import TgAccount
from config.settings import DOMAIN


def respond(update, telegram_account):
    if (
        telegram_account.temporary_token
        and telegram_account.temporary_token_expiration >= now()
    ):
        temporary_token = telegram_account.temporary_token
        remaining = int(
            (telegram_account.temporary_token_expiration - now()).total_seconds()
        )
        response_message = (
            f"https://{DOMAIN}{reverse('activate_session', args=[temporary_token])}\n"
            f"This link will expire in {remaining} seconds"
        )
    else:
        temporary_token = secrets.token_urlsafe(8)
        expiration_time = now() + timedelta(minutes=1)
        telegram_account.temporary_token = temporary_token
        telegram_account.temporary_token_expiration = expiration_time
        telegram_account.save()
        response_message = (
            f"Authenticated!"
            f" You can log in via https://{DOMAIN}{reverse('activate_session', args=[temporary_token])}"
            "\nThis link expires in 1 minute"
        )
    update.message.reply_text(response_message, disable_web_page_preview=True)
    return JsonResponse({"status": "ok", "message": response_message})


def activate_session(request, temporary_token):
    telegram_account = TgAccount.objects.filter(temporary_token=temporary_token).first()

    if telegram_account:
        if telegram_account.temporary_token_expiration >= now():
            user = telegram_account.profile.user
            if user:
                auth_login(request, user)
                telegram_account.temporary_token = None
                telegram_account.temporary_token_expiration = None
                telegram_account.save()
                return redirect("/")
        telegram_account.temporary_token = None
        telegram_account.temporary_token_expiration = None
        telegram_account.save()
        return JsonResponse({"status": "error", "message": "Token expired"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid token"}, status=400)
