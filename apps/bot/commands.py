from django.contrib.auth import get_user_model

from apps.bot.helpers import profile_with_telegram, sync_data
from apps.bot.views import login, logout, me, sessions, signup
from apps.tg_accounts.models import TgAccount

User = get_user_model()


def start_command(update, context):
    update.message.reply_text(
        f"Hi, {update.message.from_user.first_name}! How can I help you?\n\n"
        f"Check commands in the menu"
    )


def authenticate_command(update, context):
    telegram_id = update.effective_user.id
    profile = profile_with_telegram(telegram_id)
    if profile:
        login(profile, update)
    else:
        profile = signup(update)
        login(profile, update)


def me_command(update, context):
    telegram_id = update.effective_user.id
    if not profile_with_telegram(telegram_id):
        update.message.reply_text("You are unauthorized")
    else:
        me(update, profile_with_telegram(telegram_id))


def unidentified_command(update, context):
    update.message.reply_text("Sorry, I don’t recognize that command")


def logout_command(update, context):
    logout(update)


def link_command(update, user_id):
    telegram_id = update.effective_user.id
    if user_id:
        user = User.objects.filter(id=user_id).first()
        if not profile_with_telegram(telegram_id):
            telegram_account = TgAccount.objects.create(
                telegram_id=telegram_id, profile=user.profile
            )
            sync_data(telegram_account, update)
            update.message.reply_text(
                "Done!\n"
                "Your Telegram account has been successfully linked to your website profile"
            )
        else:
            update.message.reply_text(
                "Apologies, but this Telegram account is already in use\n"
                "Please log in or use a different one"
            )


def sessions_command(update, context):
    telegram_id = update.effective_user.id
    if not profile_with_telegram(telegram_id):
        update.message.reply_text("You are unauthorized")
    else:
        sessions(update, profile_with_telegram(telegram_id))
