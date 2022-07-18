from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import categories
from keyboards import kb


class Cat(StatesGroup):
    name = State()
    aliases = State()


class Del(StatesGroup):
    name = State()


async def cat_start(message: types.Message):
    await Cat.name.set()
    await message.reply('Придумайте имя для категории 💬', reply_markup=kb.canc)


async def cancel_handler_cat(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('👌', reply_markup=kb.main_m)


async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Cat.next()
    await message.reply('Придумайте ключевые слова для этой категории 💬\
                        \n(Например: Метро, автобус, проезд ...)', reply_markup=kb.canc)


async def get_aliases(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    async with state.proxy() as data:
        data['aliases'] = message.text
        await categories.new_categories(data, id_user)
    await state.finish()
    c = data['name']
    await message.answer(f'Добавлена категория <i>{c}</i> ✔', reply_markup=kb.main_m)


async def dele_cat(message: types.Message):
    await Del.name.set()
    await message.reply('Какую категорию удалить?', reply_markup=kb.canc)


async def del_name(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    async with state.proxy() as data:
        data['name'] = message.text
        await categories.delete_catt(data, id_user)
    await message.answer('Удалил 🫡', reply_markup=kb.main_m)

    await state.finish()


def register_handlers_add(dp: Dispatcher):
    dp.register_message_handler(cat_start, Text(equals=['Добавить']))
    dp.register_message_handler(cancel_handler_cat, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler_cat, Text(equals=['Отмена'], ignore_case=True), state='*')
    dp.register_message_handler(get_name, state=Cat.name)
    dp.register_message_handler(get_aliases, state=Cat.aliases)
    dp.register_message_handler(dele_cat, Text(equals=['Удалить']))
    dp.register_message_handler(del_name, state=Del.name)