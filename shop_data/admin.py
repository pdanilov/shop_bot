from django.contrib import admin

from .models import Item, User


@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "referral_id", "budget")


@admin.register(Item)
class ItemAdminModel(admin.ModelAdmin):
    list_display = ("id", "title", "price")
