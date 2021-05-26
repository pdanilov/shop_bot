import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from bot.misc import dp
from bot.utils import db
from bot.utils.keyboards import MenuActionCB, show_main_menu
from shop_bot import settings


@dp.message_handler(CommandStart(deep_link=re.compile(r"user_\d+")), state="*")
async def cmd_start_referral(message: types.Message):
    user_id = message.from_user.id
    match = re.findall(r"\d+", message.get_args())[0]
    referral_id = int(match)
    is_admin = user_id in settings.ADMINS

    if not is_admin and not await db.is_valid_referral(referral_id):
        await message.answer(
            "\n".join(
                "Неверная реферальная ссылка. Доступ запрещен."
                "Попробуйте другую ссылку, либо введите реферальный код здесь."
            )
        )
        return

    is_new = await db.add_user(user_id, referral_id)
    if is_new:
        await message.answer("Вы успешно добавлены в базу пользователей.")
    await db.update_budget(referral_id)
    await show_main_menu(message.from_user.id, message.chat.id)


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    is_admin = user_id in settings.ADMINS

    if not is_admin:
        await message.answer(
            "Вы не можете пользоваться ботом, нужно зарегистрироваться, "
            "либо ввести реферальный код вручную."
        )
        return

    is_new = await db.add_user(user_id, referral_id=None)
    if is_new:
        await message.answer("Вы успешно добавлены в базу пользователей.")
    await show_main_menu(message.from_user.id, message.chat.id)


@dp.message_handler(regexp=r"^\d+$")
async def referral_code(message: types.Message):
    user_id = message.from_user.id
    referral_id = int(message.text)

    if not await db.is_valid_referral(referral_id):
        await message.answer(
            "\n".join(
                "Неверная реферальный код. Доступ запрещен."
                "Попробуйте другой код, либо перейдите по реферальной ссылке."
            )
        )
        return

    referral_id = int(referral_id)
    is_new = await db.add_user(user_id, referral_id)
    if is_new:
        await message.answer("Вы успешно добавлены в базу пользователей.")
    await db.update_budget(referral_id)
    await show_main_menu(message.from_user.id, message.chat.id)


@dp.callback_query_handler(MenuActionCB.filter(action="referral"))
async def cq_generate_referral_link(query: types.CallbackQuery):
    bot_name = (await query.bot.get_me())["username"]
    user_id = query.from_user.id
    await query.message.answer(f"https://t.me/{bot_name}?start=user_{user_id}")
    await query.answer(cache_time=10)
