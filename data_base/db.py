import psycopg2 as pg
from typing import Dict, List, Tuple
import expenses

connect = pg.connect(dbname='finance', user='ivylou', password='peru1994peru')
cursor = connect.cursor()

cursor.execute('DROP TABLE IF EXISTS category CASCADE')
connect.commit()


cursor.execute(
    'CREATE TABLE IF NOT EXISTS category (codename VARCHAR(255) PRIMARY KEY, name VARCHAR(255),\
is_base_expense BOOLEAN, aliases TEXT)')
connect.commit()


cursor.executemany('INSERT INTO category VALUES (%s, %s, %s, %s)', (
    ('products', 'продукты', True, 'еда, пятерочка, магнит, верный, кб, перекресток, дикси'),
    ('cafe', 'кафе', False, 'кафе, мак, бк, кфс, вольчека, булочная, ресторан,'),
    ('entertainment', 'развлечения', False, 'кино, парк, музей, выставка, концерт, театр, кальян, клуб, тусовка'),
    ('rent', 'аренда и ку', True, 'кв, ку, аренда, квартира, электричество, коммуналка'),
    ('credit pay', 'кредиты', True, 'кред, платеж, кредит, ипотека'),
    ('health', 'здоровье', False, 'аптека, врач, лечение, лекарство, таблетки'),
    ('sport', 'спорт', True, 'зал, спортзал, спортпит, абонемент, тренер'),
    ('house', 'дом', True, 'ремонт, икеа, ikea, леруа'),
    ('pets', 'питомцы', False, 'корм, ветеринар, ветаптека'),
    ('transport', 'транспорт', True, 'автобус, метро, трамвай, электричка, проезд'),
    ('car', 'машина', False, 'бенз, бензин, ремонт, обслуживание, каршеринг, карш'),
    ('taxi', 'такси', False, 'убер, uber, яндекстакси, ситимобил'),
    ('clothes', 'одежда', False, 'обувь, шоппинг'),
    ('mobile', 'связь', True, 'интернет, телефон, теле2, билайн, мтс, йота'),
    ('gifts', 'подарки', False, 'др, подарок, сюрприз'),
    ('subscribes', 'подписки', True, 'яндекс, музыка, эпплмьюзик, вк, фильмы'),
    ('other', 'прочее', False, '')
))
connect.commit()


cursor.execute(
    'CREATE TABLE IF NOT EXISTS expense (id SERIAL NOT NULL PRIMARY KEY, amount INTEGER,\
created TIMESTAMP, category_codename VARCHAR(255),\
raw_text TEXT, id_user TEXT, FOREIGN KEY(category_codename) REFERENCES category(codename))')
# cursor.execute('CREATE INDEX IF NOT EXISTS id_userIndex ON expense(id_user ASC)')
connect.commit()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join(["%s"] * len(column_values.keys()))
    cursor.executemany(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values)
    connect.commit()


def fetchall(table: str, columns: List[str]):
    columns_joined = ', '.join(columns)
    rows = cursor.execute(f'SELECT {columns_joined} FROM {table}')
    rows = cursor.fetchall()
    result = []
    for i in rows:
        dict_i = {}
        for index, column in enumerate(columns):
            dict_i[column] = i[index]
        result.append(dict_i)
    return result


def delete(table: str, row_id: int, id_user: str):
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE id = {row_id} AND id_user = '{id_user}'")
    connect.commit()


def get_l(id_user: str):
    last = cursor.execute(f"SELECT expense.id, expense.amount, category.name, expense.created FROM expense\
    LEFT JOIN category ON category.codename = expense.category_codename WHERE id_user = '{id_user}'\
    ORDER BY created DESC LIMIT 5")
    last = cursor.fetchall()
    return last


def get_today_all(id_user: str):
    today = cursor.execute(f"SELECT SUM (amount) FROM expense WHERE DATE(created)=DATE(current_date)\
                           AND id_user = '{id_user}'")
    today = cursor.fetchone()
    return today


def get_today_all_categories(id_user: str):
    today1 = cursor.execute(f"SELECT category.name FROM expense LEFT JOIN category\
    ON category.codename = expense.category_codename WHERE DATE(created)=DATE(current_date)\
                            AND id_user = '{id_user}'")
    today1 = cursor.fetchall()
    res = [', '.join(i)for i in today1]
    res = set(res)
    sum1 = []
    for name in res:
        x = cursor.execute(f"SELECT SUM (expense.amount), category.name FROM expense LEFT JOIN category\
        ON category.codename = expense.category_codename WHERE DATE(created)=DATE(current_date)\
        AND id_user = '{id_user}' AND category_codename IN\
        (SELECT codename FROM category WHERE name = '{name}') GROUP BY category.name;")
        x = cursor.fetchone()
        sum1.append(x)
    # sum1 = [cursor.execute(f"SELECT expense.amount, category.name FROM expense LEFT JOIN category\
    # ON category.codename = expense.category_codename WHERE DATE(created)=DATE(current_date)\
    # AND id_user = '{id_user}' AND category_codename IN\
    # (SELECT codename FROM category WHERE name = '{name}')")for name in res]
    return sum1


def get_month_all(id_user: str):
    now = expenses._get_now_dt()
    first_day = f'{now.year:04d}-{now.month:02d}-01'
    month = cursor.execute(f"SELECT SUM (amount) FROM expense WHERE DATE(created) >= '{first_day}'\
    AND id_user = '{id_user}'")
    month = cursor.fetchone()
    return month


def get_month_all_categories(id_user: str):
    now = expenses._get_now_dt()
    first_day = f'{now.year:04d}-{now.month:02d}-01'
    month1 = cursor.execute(f"SELECT category.name FROM expense LEFT JOIN category\
    ON category.codename = expense.category_codename WHERE DATE(created) >= '{first_day}'\
    AND id_user = '{id_user}'")
    month1 = cursor.fetchall()
    res = [', '.join(i)for i in month1]
    res = set(res)
    month = []
    for name in res:
        x = cursor.execute(f"SELECT SUM (expense.amount), category.name FROM expense LEFT JOIN category\
    ON category.codename = expense.category_codename WHERE DATE (created) >= '{first_day}'\
    AND id_user = '{id_user}' AND category_codename IN\
    (SELECT codename FROM category WHERE name = '{name}') GROUP BY category.name;")
        x = cursor.fetchone()
        month.append(x)
    return month



