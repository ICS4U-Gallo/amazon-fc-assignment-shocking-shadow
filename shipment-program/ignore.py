"""
class Shelf:

    def __init__(self, categories: List[str]):
        self.categories = categories

        if not isinstance(self.categories, list):
            raise TypeError('Categories must be of type list')
        else:
            self.contents = {}
            for category in self.categories:
                self.contents.update({category: []})

    def insert_item(self, item: Item):
        try:
            self.contents[item.category].append(item)
        except KeyError:
            self.contents.update({item.category: [item]})

    def remove_item(self, **kwargs):
        self.contents[kwargs['column']].pop(kwargs['index'])

    def find_item(self, item: Item) -> int:
        pass

    def force_insert(self, item: Item, **kwargs):
        try:
            self.contents[kwargs['category']][kwargs['index']] = item
        except IndexError:
            pass  # Not Finished

    @property
    def get_contents(self) -> Dict:
        return self.contents

    def set_contents(self, contents: Dict):
        if not isinstance(contents, dict):
            raise TypeError('Contents must be of type dict')
        else:
            self.contents = contents
"""
