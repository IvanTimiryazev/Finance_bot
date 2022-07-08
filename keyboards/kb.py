from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

'''Main menu'''
main_m = ReplyKeyboardMarkup(resize_keyboard=True)

m1 = KeyboardButton('Статистика')
m2 = KeyboardButton('Как пользоваться?')
m3 = KeyboardButton('Категории')

main_m.add(m1).add(m3).add(m2)


'''Statistics block'''
stat_k = ReplyKeyboardMarkup(resize_keyboard=True)

sm = KeyboardButton('Месяц')
sd = KeyboardButton('Сегодня')
sl = KeyboardButton('Недавние траты')
sdl = KeyboardButton('Удалить все')
btm = KeyboardButton('🔙Назад в меню')

stat_k.add(sd).add(sm).add(sl).add(sdl).add(btm)


'''Delete all func'''
del_all_kb = ReplyKeyboardMarkup(resize_keyboard=True)

dyes = KeyboardButton('✔Удалить')
dno = KeyboardButton('🔙Назад в меню')

del_all_kb.add(dyes, dno)


'''Category's settings'''
cat_set = ReplyKeyboardMarkup(resize_keyboard=True)

cadd = KeyboardButton('Добавить')
cdel = KeyboardButton('Удалить')
cback = KeyboardButton('🔙Назад в меню')

cat_set.add(cadd, cdel).add(cback)


'''Cancel State machine'''
canc = ReplyKeyboardMarkup(resize_keyboard=True)

c_canc = KeyboardButton('Отмена')

canc.add(c_canc)




