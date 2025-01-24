import json
from queue import Queue

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, BotCommand, Update
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler

from apps.bot.commands import (
    authenticate_command,
    link_command,
    logout_command,
    me_command,
    sessions_command,
    start_command,
    unidentified_command,
)
from apps.bot.redis_client import get_user_from_session
from config.settings import DOMAIN, TELEGRAM_BOT_TOKEN

User = get_user_model()

bot = Bot(token=TELEGRAM_BOT_TOKEN)
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue, 4)


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update_data = json.loads(request.body)
        message = update_data.get("message", {})
        text = message.get("text", "")
        update = Update.de_json(update_data, bot)

        session_id = text.split(" ")[1] if " " in text else ""
        if session_id and (user := get_user_from_session(session_id)):
            link_command(update, user.id)

        dispatcher.process_update(update)

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def register_handlers():
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("authenticate", authenticate_command))
    dispatcher.add_handler(CommandHandler("logout", logout_command))
    dispatcher.add_handler(CommandHandler("me", me_command))
    dispatcher.add_handler(CommandHandler("link", link_command))
    dispatcher.add_handler(CommandHandler("sessions", sessions_command))

    dispatcher.add_handler(MessageHandler(Filters.command, unidentified_command))


def register_commands():
    commands = [
        BotCommand("authenticate", f"Authentication at {DOMAIN}"),
        BotCommand("logout", "Force log out of your recent sessions"),
        BotCommand("me", "Your info"),
        BotCommand("sessions", "Your sessions"),
    ]
    bot.set_my_commands(commands)


register_handlers()
register_commands()
