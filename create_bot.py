from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
