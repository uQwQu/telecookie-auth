import secrets

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.tg_accounts.models import TgAccount
from config.settings import TELEGRAM_BOT_USERNAME


def index(request):
    context = {
        "TELEGRAM_BOT_USERNAME": TELEGRAM_BOT_USERNAME,
    }
    return render(request, "tg_accounts/index.html", context)


@login_required
def telegram_linking(request):
    token = secrets.token_urlsafe()
    TgAccount.objects.create(temporary_token=token, profile=request.user.profile)
    return redirect(f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={token}")


def telegram_signup(request):
    token = secrets.token_urlsafe()
    TgAccount.objects.create(temporary_token=token)
    return redirect(f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={token}")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("/")
