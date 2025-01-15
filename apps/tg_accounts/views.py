from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from config.settings import TELEGRAM_BOT_USERNAME


def index(request):
    context = {
        "TELEGRAM_BOT_USERNAME": TELEGRAM_BOT_USERNAME,
    }
    if request.user.is_authenticated:
        context["email"] = (
            request.user.email if not request.user.email.isdigit() else ""
        )
    return render(request, "tg_accounts/index.html", context)


@login_required
def telegram_linking(request):
    return redirect(
        f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={request.session.session_key}"
    )


def telegram_auth(request):
    return redirect(f"https://t.me/{TELEGRAM_BOT_USERNAME}?start")
