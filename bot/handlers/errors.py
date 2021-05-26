from aiogram import types
from loguru import logger

from bot.misc import dp


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception(f"Cause exception {e} in update {update}")
    return True
