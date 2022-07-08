import aiogram
import asyncio
from aiogram.utils import executor
from create_bot import dp
from handlers import other, add_category


async def on_startup(_):
    print('Бот вышел в онлайн')


add_category.register_handlers_add(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)