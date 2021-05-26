from django.core.management.base import BaseCommand

from bot import misc
from bot.misc import dp
from bot.utils.executor import executor


class Command(BaseCommand):
    def handle(self, *args, **options):
        misc.setup()
        executor.start_polling(dp)
