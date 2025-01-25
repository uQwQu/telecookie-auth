from apps.profiles.models import Profile


def profile_with_telegram(telegram_id):
    profile = Profile.objects.filter(tg__telegram_id=telegram_id).first()
    return profile


def sync_data(telegram_account, update):
    user = update.effective_user
    telegram_account.username = user.username
    telegram_account.first_name = user.first_name
    telegram_account.last_name = user.last_name
    telegram_account.save()
