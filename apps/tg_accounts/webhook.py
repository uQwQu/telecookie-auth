import json

from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from apps.profiles.models import Profile
from apps.tg_accounts.models import TgAccount
from apps.tg_accounts.services import respond, send_message, sync_data
from apps.users.models import User


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", {})
        chat = message.get("chat", {})
        text = message.get("text", "")
        token = text.split(" ")[1] if " " in text else None

        telegram_account = TgAccount.objects.filter(temporary_token=token).first()
        profile_exists = Profile.objects.filter(tg__telegram_id=chat["id"]).first()

        if text.startswith("/start"):
            return start(profile_exists, telegram_account, chat, request)
    return JsonResponse({"error": "Invalid request"}, status=400)


def start(profile_exists, telegram_account, chat, request):
    if profile_exists:
        if telegram_account and telegram_account.profile != profile_exists:
            telegram_account.delete()
            response_message = (
                "Apologies, but this Telegram account is already in use."
                " Please log in or use a different one."
            )
            send_message(chat["id"], response_message)
            return JsonResponse({"status": "ok", "message": response_message})
        # Login
        return login(profile_exists, chat, request)
    else:
        if not telegram_account:
            response_message = "It looks like you’re not signed up"
            send_message(chat["id"], response_message)
            return JsonResponse({"status": "ok", "message": response_message})
        # Linking/Signup
        return linking_signup(telegram_account, chat, request)


def login(profile_exists, chat, request):
    telegram_account = TgAccount.objects.get(profile=profile_exists)
    sync_data(telegram_account, chat)
    return respond(telegram_account, chat, request)


def linking_signup(telegram_account, chat, request):
    sync_data(telegram_account, chat)

    if not telegram_account.profile:
        username = chat.get("username", "")
        if User.objects.filter(username=username).exists() or not username:
            username += get_random_string(length=5)
        user = User.objects.create(
            username=username,
            first_name=chat.get("first_name"),
            last_name=chat.get("last_name", ""),
            email=f"{chat.get("id")}@fake.email",
        )
        telegram_account.profile = user.profile
        telegram_account.profile.user = user

    return respond(telegram_account, chat, request)
