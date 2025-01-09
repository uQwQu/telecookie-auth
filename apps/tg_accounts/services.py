import secrets
from datetime import timedelta

import requests
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now

from apps.tg_accounts.models import TgAccount
from config.settings import TELEGRAM_BOT_TOKEN


def sync_data(telegram_account, chat):
    telegram_account.telegram_id = chat["id"]
    telegram_account.username = chat.get("username")
    telegram_account.first_name = chat.get("first_name")
    telegram_account.last_name = chat.get("last_name")
    telegram_account.save()


def respond(telegram_account, chat, request):
    temporary_token = secrets.token_urlsafe(8)
    expiration_time = now() + timedelta(minutes=1)
    telegram_account.temporary_token = temporary_token
    telegram_account.temporary_token_expiration = expiration_time
    telegram_account.save()
    response_message = (
        "You’ve been successfully authenticated! Click the link below to log in to the website:"
        f"\nhttps://{request.get_host()}{reverse('activate_session', args=[temporary_token])}"
    )
    send_message(chat["id"], response_message)
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


def send_message(chat_id, response_message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": response_message,
        "disable_web_page_preview": True,
    }
    requests.post(url, json=payload)
