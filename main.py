import aiogram
import asyncio
from aiogram.utils import executor
from create_bot import dp
from handlers import other, add_category
import logging.config

logging.config.fileConfig(fname='logging.conf')
logger = logging.getLogger(__name__)
loggerInfo = logging.getLogger('logInfo')


async def on_startup(_):
    loggerInfo.info('Bot online')


add_category.register_handlers_add(dp)
other.register_handlers_other(dp)

try:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
except Exception:
    logger.exception('Not connected')