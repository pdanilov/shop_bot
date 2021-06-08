from decimal import Decimal
from typing import Optional, Union

from asgiref.sync import sync_to_async

from shop_data.models import Item, User


@sync_to_async
def add_user(user_id: int, referral_id: Union[int, None], budget: Optional[int] = 0):
    try:
        User.objects.get(telegram_id=user_id)
        created = False
    except User.DoesNotExist:
        User.objects.create(telegram_id=user_id, referral_id=referral_id, budget=budget)
        created = True

    return created


@sync_to_async
def is_valid_referral(referral_id: int):
    try:
        User.objects.get(telegram_id=referral_id)
        is_valid = True
    except User.DoesNotExist:
        is_valid = False

    return is_valid


@sync_to_async
def update_budget(user_id: int, delta: Optional[Union[int, float]] = 10):
    user = User.objects.get(telegram_id=user_id)
    user.budget += Decimal(delta)
    user.save()


@sync_to_async
def item_search(text: str):
    results = Item.objects.order_by("title")
    if len(text) >= 2:
        results = results.filter(title__icontains=text)
    return [*results]


@sync_to_async
def get_user(telegram_id: int):
    return User.objects.get(telegram_id=telegram_id)


@sync_to_async
def get_item(item_id: int):
    return Item.objects.get(id=item_id)
