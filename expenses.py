import datetime
import re
from typing import NamedTuple, Optional
import exceptions
import pytz
from data_base import db
from categories import Categories
import logging

logging.basicConfig(filename='logging.log', level='ERROR')
logger = logging.getLogger(__name__)


class Message(NamedTuple):
    amount: int
    category_text: str


class Expense(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


class Static(NamedTuple):
    amount: int
    name: str


class Expense2(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str
    time: str


def add_expenses(raw_message: str, id_user: str):
    parsed_m = _parse_message(raw_message)
    category = Categories(id_user).get_category(parsed_m.category_text)
    if not category:
        raise exceptions.NotCorrectCategory('Такой категории пока нет.\nСоздай нужную категорию или категорию \
                                            "Прочее" для трат без категории.')

    inserted_row = db.insert('expense', {'amount': parsed_m.amount, 'created': _get_now_f(),
                                         'category_codename': category.codename, 'raw_text': raw_message,
                                         'id_user': id_user})

    return Expense(id=None, amount=parsed_m.amount, category_name=category.name)


def _parse_message(raw_message: str):
    parse_result = re.match(r"([\d]+) (.*)", raw_message)
    if not parse_result or not parse_result.group(0) or not parse_result.group(1) or not parse_result.group(2):
        raise exceptions.NotCorrectMessage('Не могу понять:(\nНапишите сообщение в формате сумма категория, например:\
                                           \n300 такси')

    amount = parse_result.group(1).replace(' ', '')
    category_text = parse_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def delete_exp(row_id: int, id_user: str):
    db.delete('expense', row_id, id_user)


def del_all(id_user: str):
    db.delete_all(id_user)


def get_last(id_user: str):
    last = db.get_l(id_user)
    recent_pays = [Expense2(id=i[0], amount=i[1], category_name=i[2], time=i[3])for i in last]
    return recent_pays


def get_today(id_user: str):
    today = db.get_today_all(id_user)
    all_td = today[0]
    return all_td


def get_today_categories(id_user: str):
    today = db.get_today_all_categories(id_user)
    static = [Static(amount=i[0], name=i[1])for i in today]
    return static


def get_month(id_user: str):
    month = db.get_month_all(id_user)
    all_m = month[0]
    return all_m


def get_month_categories(id_name: str):
    month = db.get_month_all_categories(id_name)
    static = [Static(amount=i[0], name=i[1])for i in month]
    return static


def _get_now_f():
    return _get_now_dt().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_dt():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    return now
