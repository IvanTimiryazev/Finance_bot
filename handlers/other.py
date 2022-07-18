from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import exceptions
from create_bot import dp, bot
import expenses
import categories
from keyboards.kb import main_m, stat_k, del_all_kb, cat_set
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_w(message: types.Message):
    await message.answer('<b>Бот для учета финансов</b>\n\nВведите трату:', reply_markup=main_m)


async def stat(message: types.Message):
    await message.answer('<b>Твоя статистика📊</b>', reply_markup=stat_k)


async def back_m(message: types.Message):
    await message.answer('<b>Бот для учета финансов</b>\n\nВведите трату:', reply_markup=main_m)


async def del_all(message: types.Message):
    await message.answer('а ю шуре❓', reply_markup=del_all_kb)


async def dyes(message: types.Message):
    id_user = message.from_user.id
    expenses.del_all(id_user)
    await message.answer('Удалил 🫡', reply_markup=main_m)


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


async def del_callback(callback: types.CallbackQuery):
    id_user = callback.from_user.id
    row_id = int(callback.data.replace('del', ''))
    expenses.delete_exp(row_id, id_user)
    await callback.answer(text='Удалил🗑', show_alert=True)


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


async def get_cat(message: types.Message):
    id_user = message.from_user.id
    c = categories.Categories(id_user).get_all_cat(id_user)
    m = '\n* '.join([f'<b>{i.name}</b>' + ' (' + ', '.join(i.aliases) + ')'for i in c])
    await message.answer('<b>Категории трат📋</b>' + '\n\n' + '* ' + m, reply_markup=cat_set)


async def how(message: types.Message):
    await message.answer(
        '<b>Немного о боте</b>\n\n<b>Что делает этот бот?</b>👀\nЭто бот - финансовый асистент. Он сохраняет ваши \
траты, распределяет по категориям, а так же выводит статистику.\n\n<b>Как внести трату?📒</b>\nПросто введите сообщение в\
 формате: "Сумма категория". Например: 300 такси.\n\n<b>Как создать категорию?🤔</b>\nДобавляйте нужные вам категории!\
 Заходите в раздел "Категории", и нажмите "Добавить". Там же вы можете удалить категорию.\n(При удалении категории, \
все траты из этой категории будут удалены.)\n\n<b>Бот бесплатный?</b>💸\nДа'
    )


async def add_exp(message: types.Message):
    id_user = message.from_user.id
    try:
        expense = expenses.add_expenses(message.text, id_user)
    except exceptions.NotCorrectMessage as ex:
        await message.answer(str(ex))
    except exceptions.NotCorrectCategory as ec:
        await message.answer(str(ec))

        return
    await message.answer(f'добавлены траты {expense.amount} на {expense.category_name}')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(start_w, commands=['start'])
    dp.register_message_handler(stat, Text(equals=['Статистика']))
    dp.register_message_handler(back_m, Text(equals=['🔙Назад в меню']))
    dp.register_message_handler(del_all, Text(equals=['Удалить все']))
    dp.register_message_handler(dyes, Text(equals=['✔Удалить']))
    dp.register_message_handler(get_last_exp, Text(equals=['Недавние траты']))
    dp.register_callback_query_handler(del_callback, Text(startswith='del'))
    dp.register_message_handler(get_all_today, Text(equals=['Сегодня']))
    dp.register_message_handler(get_all_m, Text(equals=['Месяц']))
    dp.register_message_handler(get_cat, Text(equals=['Категории']))
    dp.register_message_handler(how, Text(equals=['Как пользоваться?']))
    dp.register_message_handler(add_exp)