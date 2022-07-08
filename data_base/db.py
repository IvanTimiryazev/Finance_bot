import psycopg2 as pg
from typing import Dict, List
import expenses

connect = pg.connect(dbname='finance', user='ivylou', password='peru1994peru')
cursor = connect.cursor()

# cursor.execute('DROP TABLE IF EXISTS category CASCADE')
# cursor.execute('DROP TABLE IF EXISTS expense CASCADE')
# connect.commit()


cursor.execute(
    'CREATE TABLE IF NOT EXISTS category (codename VARCHAR(255), name VARCHAR(255),\
is_base_expense BOOLEAN, aliases TEXT, id_user_c TEXT, codename_id BIGSERIAL NOT NULL PRIMARY KEY)')
cursor.execute('CREATE INDEX IF NOT EXISTS id_user_c ON category(id_user_c)')
connect.commit()


cursor.execute(
    'CREATE TABLE IF NOT EXISTS expense (id BIGSERIAL NOT NULL PRIMARY KEY, amount INTEGER,\
created TIMESTAMP, category_codename VARCHAR(255),\
raw_text TEXT, id_user TEXT, codename_id_category INTEGER,\
FOREIGN KEY(codename_id_category) REFERENCES category(codename_id))')
cursor.execute('CREATE INDEX IF NOT EXISTS id_user ON expense(id_user)')
connect.commit()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join(["%s"] * len(column_values.keys()))
    cursor.executemany(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values)
    connect.commit()


def insert_cat(column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join(["%s"] * len(column_values.keys()))
    cursor.executemany(f'INSERT INTO category VALUES ({placeholders})', values)
    connect.commit()


def fetchall(columns: List[str], id_user: str):
    columns_joined = ', '.join(columns)
    rows = cursor.execute(f"SELECT {columns_joined} FROM category WHERE id_user_c = '{id_user}'")
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


def delete_all(id_user: str):
    cursor.execute(f"DELETE FROM expense WHERE id_user = '{id_user}'")
    connect.commit()


def get_l(id_user: str):
    last = cursor.execute(f"SELECT expense.id, expense.amount, category.name, expense.created FROM expense\
    LEFT JOIN category ON category.codename = expense.category_codename AND category.id_user_c = expense.id_user\
    WHERE id_user = '{id_user}' ORDER BY created DESC LIMIT 5")
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
        ON category.codename = expense.category_codename AND category.id_user_c = expense.id_user\
        WHERE DATE(created)=DATE(current_date)\
        AND id_user = '{id_user}' AND category_codename IN\
        (SELECT codename FROM category WHERE name = '{name}') GROUP BY category.name")
        x = cursor.fetchone()
        sum1.append(x)
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
    ON category.codename = expense.category_codename AND category.id_user_c = expense.id_user\
    WHERE DATE (created) >= '{first_day}' AND id_user = '{id_user}' AND category_codename IN\
    (SELECT codename FROM category WHERE name = '{name}') GROUP BY category.name;")
        x = cursor.fetchone()
        month.append(x)
    return month


def delete_cat(name: str, id_user: str):
    cursor.execute(f"DELETE FROM expense WHERE category_codename IN\
    (SELECT codename FROM category WHERE name = '{name}')")
    cursor.execute(f"DELETE FROM category WHERE name = '{name}' AND id_user_c = '{id_user}'")
    connect.commit()
