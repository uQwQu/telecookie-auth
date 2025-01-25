from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from apps.tg_accounts.bot.helpers import sync_data
from apps.tg_accounts.bot.redis_client import get_active_sessions, get_sessions_data, redis_client
from apps.tg_accounts.bot.services import respond
from apps.tg_accounts.models import TgAccount

User = get_user_model()


def login(update, profile_exists):
    telegram_account = TgAccount.objects.get(profile=profile_exists)
    sync_data(telegram_account, update)
    return respond(update, telegram_account)


def logout(update, profile):
    active_sessions = get_active_sessions(profile)
    if active_sessions:
        for session_id in active_sessions:
            redis_client.delete(f":1:django.contrib.sessions.cache{session_id}")
        update.message.reply_text("You have logged out successfully")
    else:
        update.message.reply_text("You are unauthorized")


def signup(update):
    telegram_account = TgAccount.objects.create(telegram_id=update.effective_user.id)
    sync_data(telegram_account, update)
    effective_user = update.effective_user
    username = effective_user.username or ""
    if User.objects.filter(username=username).exists() or not username:
        username += get_random_string(length=5)
    user = User.objects.create(
        username=username,
        first_name=effective_user.first_name,
        last_name=effective_user.last_name or "",
        email=effective_user.id,
    )
    telegram_account.profile = user.profile
    telegram_account.profile.user = user
    telegram_account.save()
    return telegram_account.profile


def me(update, profile):
    user = profile.user
    last_name = user.last_name if user.last_name else ""
    email = user.email if not user.email.isdigit() else ""
    last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
    admin = "admin\n\n" if user.is_staff else ""
    message = (
        f"<b>Profile Information</b>\n\n"
        f"{user.first_name} {last_name}\n\n"
        f"Username: {user.username}\n\n"
    )
    if email:
        message += f"Email: {email}\n\n"
    if admin:
        message += admin
    message += f"Last login: {last_login}\n\n"

    update.message.reply_text(message, parse_mode="HTML")


def sessions(update, profile):
    sessions_data = get_sessions_data(profile)

    sessions_info = []
    for session, session_id, creation_datetime in sessions_data:
        if creation_datetime:
            formatted_creation = creation_datetime.strftime("%Y-%m-%d %H:%M:%S")
            current_time = datetime.now(pytz.utc)
            time_difference = current_time - creation_datetime
            days, remainder = divmod(time_difference.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_diff_str = (
                f"{int(days)} days, {int(hours)}:{int(minutes):02}:{int(seconds):02}"
            )
            sessions_info.append(
                f"Session from {formatted_creation}\nDuration: {time_diff_str}\n\n"
            )
    if sessions_info:
        update.message.reply_text(
            "<b>Your active sessions</b>\n\n" + "".join(sessions_info),
            parse_mode="HTML",
        )
    else:
        update.message.reply_text("You have no active sessions")
