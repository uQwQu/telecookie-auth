from django.contrib import admin

from apps.tg_accounts.models import TgAccount


class TgAccountAdmin(admin.ModelAdmin):
    list_display = ["username", "telegram_id", "profile"]
    readonly_fields = ("profile",)


admin.site.register(TgAccount, TgAccountAdmin)
