from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_m = ReplyKeyboardMarkup(resize_keyboard=True)

m1 = KeyboardButton('Статистика')
m2 = KeyboardButton('Как пользоваться?')
m3 = KeyboardButton('Категории')

main_m.add(m1).add(m3).add(m2)


stat_k = ReplyKeyboardMarkup(resize_keyboard=True)

sm = KeyboardButton('Месяц')
sd = KeyboardButton('Сегодня')
sl = KeyboardButton('Недавние траты')
sdl = KeyboardButton('Удалить все')
btm = KeyboardButton('🔙Назад в меню')

stat_k.add(sd).add(sm).add(sl).add(sdl).add(btm)


del_all_kb = ReplyKeyboardMarkup(resize_keyboard=True)

dyes = KeyboardButton('✔Удалить')
dno = KeyboardButton('🔙Назад в меню')

del_all_kb.add(dyes, dno)





