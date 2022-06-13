from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import exceptions
from create_bot import dp, bot
import expenses
import categories
from keyboards.kb import main_m, stat_k
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(commands=['start'])
async def start_w(message: types.Message):
    await message.answer('<b>Бот для учета финансов</b>\n\nВведите трату:', reply_markup=main_m)


@dp.message_handler(Text(equals=['Статистика']))
async def stat(message: types.Message):
    await message.answer('<b>Твоя статистика📊</b>', reply_markup=stat_k)


@dp.message_handler(Text(equals=['🔙Назад в меню']))
async def back_m(message: types.Message):
    await message.answer('<b>Бот для учета финансов</b>\n\nВведите трату:', reply_markup=main_m)


@dp.message_handler(Text(equals=['Недавние траты']))
async def get_last_exp(message: types.Message):
    id_user = message.from_user.id
    last = expenses.get_last(id_user)
    if not last:
        await message.answer('Расходов пока не было')
        return
    await message.answer('<b>Недавние траты:</b>')
    for i in last:
        await bot.send_message(
            message.from_user.id, text=f'{i.amount} рублей на {i.category_name}({i.time})',
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('🔝Удалить', callback_data=f'del{i.id}')))


@dp.callback_query_handler(Text(startswith='del'))
async def del_callback(callback: types.CallbackQuery):
    id_user = callback.from_user.id
    row_id = int(callback.data.replace('del', ''))
    expenses.delete_exp(row_id, id_user)
    await callback.answer(text='Удалил🗑', show_alert=True)


@dp.message_handler(Text(equals=['Сегодня']))
async def get_all_today(message: types.Message):
    id_user = message.from_user.id
    today = expenses.get_today(id_user)
    if not today:
        await message.answer('Сегодня расходов не было')
        return
    today_cat = expenses.get_today_categories(id_user)
    today_cat_l = [f'<i>{i.amount} рублей на {i.name}</i>'for i in today_cat]
    m = '\n* '.join(today_cat_l)
    await message.answer(f'<b>Всего расходов сегодня:</b> {today} рублей\n\n' + '* ' + m)


@dp.message_handler(Text(equals=['Месяц']))
async def get_all_m(message: types.Message):
    id_user = message.from_user.id
    month = expenses.get_month(id_user)
    if not month:
        await message.answer('В этом месяце расходов не было')
        return
    month_cat = expenses.get_month_categories(id_user)
    month_cat_l = [f'<i>{i.amount} рублей на {i.name}</i>'for i in month_cat]
    m = '\n* '.join(month_cat_l)
    await message.answer(f'<b>Всего расходов в этом месяце:</b> {month} рублей\n\n' + '* ' + m)


@dp.message_handler(Text(equals=['Категории']))
async def get_cat(message: types.Message):
    c = categories.Categories().get_all_cat()
    m = '\n* '.join([f'<b>{i.name}</b>' + ' (' + ', '.join(i.aliases) + ')'for i in c])
    await message.answer('<b>Категории трат📋</b>' + '\n\n' + '* ' + f'<i>{m}</i>')



@dp.message_handler(Text(equals=['Как пользоваться?']))
async def how(message: types.Message):
    await message.answer(
        '<b>Немного о боте</b>\n\n<b>Что делает этот бот?</b>👀\nЭто бот - финансовый асистент. Он сохраняет ваши \
траты, распределяет по категориям, а так же выводит статистику\n\n<b>Как внести трату?📒\n</b>Просто введите сообщение в\
 формате: "Сумма категория".Например: 300 такси\n\n<b>Бот бесплатный?</b>💸\nДа'
    )


@dp.message_handler()
async def add_exp(message: types.Message):
    id_user = message.from_user.id
    try:
        expense = expenses.add_expenses(message.text, id_user)
    except exceptions.NotCorrectMessage as ex:
        await message.answer(str(ex))
        return

    await message.answer(f'добавлены траты {expense.amount} на {expense.category_name}')
