from django.db import models

from shop_bot import settings


class TimedBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimedBaseModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(
        verbose_name="Telegram ID пользователя", unique=True
    )
    referral_id = models.IntegerField(null=True)
    budget = models.DecimalField(verbose_name="Бюджет", decimal_places=2, max_digits=8)

    def __str__(self):
        return f"#{self.id} ({self.telegram_id}, {self.budget} {settings.CURRENCY})"


class Item(TimedBaseModel):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Название товара", max_length=32)
    thumb_url = models.CharField(verbose_name="Ссылка на превью", max_length=200)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=8)
    description = models.TextField(verbose_name="Описание", max_length=255, null=True)

    def __str__(self):
        return f"#{self.id} ({self.title}, {self.price})"
