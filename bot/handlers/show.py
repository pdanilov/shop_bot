import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.callback_data import CallbackData

from bot.misc import dp
from bot.utils import db
from bot.utils.keyboards import MenuActionCB, show_main_menu

ItemCB = CallbackData("item", "id")


@dp.inline_handler(state="*")
async def iq_item_search(query: types.InlineQuery):
    results = []
    bot_name = (await query.bot.get_me())["username"]

    for item in await db.item_search(query.query):
        show_button = types.InlineKeyboardButton(
            "Показать товар", url=f"https://t.me/{bot_name}?start=item_{item.id}"
        )
        buttons = [[show_button]]
        keyboard = types.InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)
        content = types.InputTextMessageContent(item.description)
        results.append(
            types.InlineQueryResultArticle(
                id=str(item.id),
                title=item.title,
                input_message_content=content,
                description=f"{item.price}$",
                thumb_url=item.thumb_url,
                reply_markup=keyboard,
            )
        )

    await query.answer(results)


@dp.message_handler(CommandStart(deep_link=re.compile(r"item_\d+")))
async def cmd_show_item(message: types.Message):
    item_id = re.findall(r"\d+", message.get_args())[0]
    buy_button = types.InlineKeyboardButton(
        "Купить", callback_data=ItemCB.new(id=item_id)
    )
    cancel_button = types.InlineKeyboardButton(
        "Отмена", callback_data=MenuActionCB.new(action="cancel")
    )
    keyboard = types.InlineKeyboardMarkup(
        row_width=1, inline_keyboard=[[buy_button, cancel_button]]
    )
    item = await db.get_item(int(item_id))
    await message.answer_photo(
        item.thumb_url,
        caption="\n".join(
            (
                f"Название: {item.title}",
                f"Стоимость: {item.price}$",
                f"Описание: {item.description}",
            )
        ),
        reply_markup=keyboard,
    )


@dp.callback_query_handler(MenuActionCB.filter(action="cancel"))
async def cq_cancel(query: types.CallbackQuery):
    await show_main_menu(query.from_user.id, query.message.chat.id)
    await query.answer()
