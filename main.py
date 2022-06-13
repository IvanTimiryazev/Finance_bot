import aiogram
import asyncio
from aiogram.utils import executor
from create_bot import dp
from handlers import other


async def on_startup(_):
    print('Бот вышел в онлайн')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)