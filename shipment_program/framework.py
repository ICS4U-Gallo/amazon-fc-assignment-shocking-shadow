from typing import List


class ShipmentError(UserWarning):
    pass


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
    def __init__(self, direction: str, number: int, destination: str, contents: List):
        self.direction = direction
        self.number = number
        self.destination = destination
        self.contents = contents

    def __str__(self):
        if self.direction == "in":
            return f"Bin number {self.number} is bringing items to shelving area."
        elif self.direction == "out":
            return f"Bin number {self.number} is bringing items to scanning area."

    def send_bin(self, truck: "Truck"):
        truck.load_bin(self)

    def item_count(self) -> int:
        return len(self.contents)

    def print_item_count(self) -> str:
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

    def if_item(self, code: int) -> bool:
        for item in self.contents:
            if code == item.code:
                return True
            else:
                return False

    def print_if_item(self, code: int) -> str:
        for item in self.contents:
            if code == item.code:
                return "item is in the bin"
            else:
                return "item is not in the bin"

    def get_item(self, code):
        for item in self.contents:
            if code == item.code:
                return item
            else:
                return -1


class Truck:

    def __init__(self, destination: str, contents=None):
        self.contents = []
        self.destination = destination

        if contents is None:
            self.contents = []
        else:
            for element in contents:
                if not isinstance(element, Bin):
                    raise TypeError('List must contain only Bins')
                else:
                    self.contents.append(element) if element.destination == self.destination else None

        self.delivery_status = False

    def is_delivered(self) -> bool:
        return self.delivery_status

    def deliver(self) -> List[Bin]:
        self.delivery_status = True
        shipment = self.contents

        self.contents = []
        return shipment

    def load_bin(self, shipment_bin: Bin):
        if shipment_bin.destination != self.destination:
            raise ShipmentError('Bin and Truck destination mismatch')
        else:
            self.contents.append(shipment_bin)

    def __str__(self) -> str:
        return 'Contents: {}, Destination: {}'.format(self.contents, self.destination)
