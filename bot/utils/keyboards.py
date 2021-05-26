from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot.misc import dp
from shop_bot import settings

MenuActionCB = CallbackData("menu", "action")


async def show_main_menu(user_id: int, chat_id: int):
    items_button = types.InlineKeyboardButton(
        "Выбрать товар", switch_inline_query_current_chat=""
    )
    referral_button = types.InlineKeyboardButton(
        "Реферал-ссылка", callback_data=MenuActionCB.new(action="referral")
    )
    admin_button = types.InlineKeyboardButton(
        "Админка django", url=f"http://{settings.APP_HOST}:{settings.DJANGO_PORT}/admin"
    )
    buttons = [[items_button, referral_button]]
    if user_id in settings.ADMINS:
        buttons.append([admin_button])
    keyboard = types.InlineKeyboardMarkup(
        row_width=len(buttons[0]), inline_keyboard=buttons
    )
    await dp.bot.send_message(chat_id, "Выбери по душе", reply_markup=keyboard)
