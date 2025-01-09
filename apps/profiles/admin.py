from django.contrib import admin

from apps.profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "user_id", "first_name", "telegram_id", "telegram_username"]
    readonly_fields = ("user",)
    list_display_links = ["first_name", "user_id"]

    def first_name(self, obj):
        return obj.user.first_name

    def user_id(self, obj):
        return obj.user.id

    def telegram_id(self, obj):
        return obj.tg.telegram_id

    def telegram_username(self, obj):
        return obj.tg.username


admin.site.register(Profile, ProfileAdmin)
