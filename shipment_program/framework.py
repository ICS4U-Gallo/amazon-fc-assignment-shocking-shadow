from typing import List


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


class Bin:
    def __init__(self, direction: str, number: int):
        self.direction = direction
        self.number = number
        self.contents = []

    def __str__(self):
        if self.direction == "in":
            return f"Bin number {self.number} is bringing items to shelving area."
        elif self.direction == "out":
            return f"Bin number {self.number} is bringing items to scanning area."

    def send_bin(self):
        pass

    def item_count(self):
        if len(self.contents) > 2:
            return f"There are {len(self.contents)} items in the bin."
        elif len(self.contents) == 1:
            return f"There is {len(self.contents)} item in the bin."
        else:
            return f"There are {len(self.contents)} items in the bin."

    def add(self, item: Item):
        self.contents.append(item)

    def remove(self, item: Item):
        self.contents.remove(item)

    def find_item(self, code: int):
        if code in self.contents:
            phrase = f"item is in the Bin."
        else:
            phrase = f"item not in Bin."
        return phrase

    def get_item(self, code):
        if code in self.contents:
            return code
