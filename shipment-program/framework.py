from typing import List, Dict, Tuple


class Item:

    def __init__(self, name=None, code=None, category=None, destination=None):
        self.name = name
        self.code = code
        self.category = category
        self.destination = destination

    def set_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError('name must be string')
        else:
            self.name = name

    def set_code(self, code: int):
        if not isinstance(code, int):
            raise TypeError('code must be int')
        else:
            self.code = code

    def set_category(self, category: str):
        if not isinstance(category, str):
            raise TypeError('category must be type str')
        else:
            self.category = category

    def set_destination(self, destination: str):
        if not isinstance(destination, str):
            raise TypeError('destination must be type str')
        else:
            self.destination = destination

    def __str__(self) -> str:
        return 'Name: {}\nCode:{}\nCategory: {}\nDestination: {}\n'.format(self.name, self.code,
                                                                           self.category, self.destination)


class Bin(list):

    def __init__(self, items: List):
        super().__init__()
        self.extend(items)


class Shelf(dict):

    def __init__(self, categories: List):
        super().__init__()
        self.categories = categories

        if not isinstance(self.categories, List):
            raise TypeError('categories must be of type list')
        else:
            for category in categories:
                self.update({category: {}})

    def insert(self, item: Item):
        try:
            self[item.category].append(item)
        except KeyError:
            self.update({item.category: [item]})

    def force_insert(self, **kwargs):
        self[kwargs['category']].update({kwargs['index']: kwargs['item']})

    def remove(self, **kwargs):
        self[kwargs['category']].pop(kwargs['index'])

    def retrieve(self, **kwargs):
        return self[kwargs['category']][kwargs['index']]
