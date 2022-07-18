import os
from dotenv import load_dotenv
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import other, add_category
import logging.config

logging.config.fileConfig(fname='logging.conf')
logger = logging.getLogger(__name__)
loggerInfo = logging.getLogger('logInfo')

load_dotenv()


async def on_startup(dp):
    await bot.set_webhook(os.getenv('WEBHOOK_HOST'))
    loggerInfo.info('Bot online')


async def on_shutdown(dp):
    await bot.delete_webhook()


add_category.register_handlers_add(dp)
other.register_handlers_other(dp)

try:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path=os.getenv('WEBHOOK_PATH'),
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=os.getenv('WEBAPP_HOST'),
    #     port=os.getenv('WEBAPP_PORT')
    # )
except Exception:
    logger.exception('Not connected')

