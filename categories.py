from typing import List, Dict, NamedTuple
from data_base import db
from transliterate import translit


class Category(NamedTuple):
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class CategoryAdd(NamedTuple):
    name: str


class Categories:
    def __init__(self, id_user: str):
        self._categories = self._load_categories(id_user)
        self.id_user = id_user

    def _load_categories(self, id_user: str):
        categories = db.fetchall('codename name is_base_expense aliases'.split(), id_user)
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]):
        categories_res = []
        for index, category in enumerate(categories):
            aliases = category['aliases'].split(',')
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category['name'])
            categories_res.append(Category(codename=category['codename'], name=category['name'],
                                           is_base_expense=category['is_base_expense'], aliases=aliases))
        return categories_res

    def get_all_cat(self, id_user: str):
        get = self._load_categories(id_user)
        return get

    def get_category(self, category_name: str):
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == 'prochee':
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded


async def new_categories(data: Dict, id_user: str):
    data_l = []
    data_l.append(data)
    for i in data_l:
        name = i['name'].lower()
        codename = translit(name, 'ru', reversed=True)
        aliases = i['aliases'].lower()
        # aliases = i['aliases'].split(',')
        # aliases = list(filter(None, map(str.strip, aliases)))
        is_base = True
    inserted_cat = db.insert_cat({'codename': codename, 'name': name, 'is_base_expense': is_base,
                                  'aliases': aliases, 'id_user_c': id_user})

    return CategoryAdd(name=name)


async def delete_catt(data: Dict, id_user: str):
    data_d = []
    data_d.append(data)
    for i in data_d:
        name = i['name'].lower()
    db.delete_cat(name, id_user)