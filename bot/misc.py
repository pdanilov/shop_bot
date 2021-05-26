from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from shop_bot import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
dp = Dispatcher(bot, storage=storage)


def setup():
    from bot import handlers
    from bot.utils import executor, logging

    executor.setup()
    logging.setup()
    handlers.setup()
