from aiogram.utils.executor import Executor
from loguru import logger

from bot.misc import dp
from bot.utils import dispatcher

executor = Executor(dp)


def setup():
    logger.info("Configure executor")
    dispatcher.setup(executor)
