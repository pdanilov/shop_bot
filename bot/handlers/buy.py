import json
import re
from typing import Union
from urllib.request import urlopen

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CurrencyTotalAmountInvalid

from bot.handlers.show import ItemCB
from bot.misc import dp
from bot.utils import db
from bot.utils.keyboards import show_main_menu
from shop_bot import settings


@dp.callback_query_handler(ItemCB.filter())
async def cq_item_quantity(
    query: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    item_id = int(callback_data["id"])
    await state.update_data(item_id=item_id)
    buttons = [[types.KeyboardButton(f"{idx}") for idx in range(1, 4)]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=len(buttons[0]),
    )
    await query.message.answer(
        "Введите количество товара или введите вручную", reply_markup=keyboard
    )
    await state.set_state("SET_ITEM_QUANTITY")
    await query.answer()


@dp.message_handler(regexp=re.compile(r"^[1-9]\d*$"), state="SET_ITEM_QUANTITY")
async def buy_item(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    item_id = (await state.get_data())["item_id"]
    item = await db.get_item(item_id)
    currency = Currency(settings.CURRENCY)
    amount = currency.to_fractional(quantity * item.price)

    try:
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title=item.title,
            description=item.description,
            payload=item_id,
            provider_token=settings.PROVIDER_TOKEN,
            currency=settings.CURRENCY,
            prices=[types.LabeledPrice(item.title, amount)],
            need_shipping_address=True,
            is_flexible=True,
        )
    except CurrencyTotalAmountInvalid:
        await currency_total_amount_invalid(message.from_user.id, message.chat.id)

    await state.finish()


@dp.shipping_query_handler()
async def sq_choose_shipping(query: types.ShippingQuery):
    shipping_options = [
        types.ShippingOption(
            id="regular_post",
            title="Почта",
            prices=[types.LabeledPrice("Обычная доставка", amount=300)],
        ),
        types.ShippingOption(
            id="express",
            title="Курьерская доставка",
            prices=[types.LabeledPrice("Экспресс-доставка", amount=600)],
        ),
    ]
    await dp.bot.answer_shipping_query(
        shipping_query_id=query.id,
        ok=True,
        shipping_options=shipping_options,
    )


@dp.pre_checkout_query_handler()
async def pcq_confirm_shipping(query: types.PreCheckoutQuery, state: FSMContext):
    user = await db.get_user(state.user)
    currency = Currency(settings.CURRENCY)
    amount = currency.to_unit(query.total_amount)

    if amount <= user.budget:
        await db.update_budget(state.user, delta=-amount)
        await dp.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    else:
        await dp.bot.answer_pre_checkout_query(
            pre_checkout_query_id=query.id,
            ok=False,
            error_message="У вас недостаточно средств для покупки.",
        )

    await show_main_menu(state.user, state.chat)


class Currency:
    def __init__(self, code: str):
        with urlopen("https://core.telegram.org/bots/payments/currencies.json") as url:
            data = json.loads(url.read().decode())
            currency_info = data[code]

        self.exp = int(currency_info["exp"])
        self.min_amount = int(currency_info["min_amount"]) // 10 ** self.exp
        self.max_amount = int(currency_info["max_amount"]) // 10 ** self.exp
        self.symbol = currency_info["symbol"]

    def to_fractional(self, amount: Union[int, float]) -> int:
        return int(amount) * 10 ** self.exp

    def to_unit(self, amount: Union[int, float]) -> float:
        return float(amount // 10 ** self.exp)


async def currency_total_amount_invalid(user_id: int, chat_id: int):
    currency = Currency(settings.CURRENCY)

    await dp.bot.send_message(
        chat_id,
        "Сумма покупки должна быть в пределах "
        f"от {currency.min_amount}{currency.symbol} "
        f"до {currency.max_amount}{currency.symbol}.",
    )
    await show_main_menu(user_id, chat_id)
