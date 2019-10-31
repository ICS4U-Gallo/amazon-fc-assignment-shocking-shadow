import shipment_program as shp


# Testing Item class

def test_set_name():
    instance = shp.Item()

    instance.set_name('Test')
    assert 'Test' == instance.name

    instance.set_name('Apple')
    assert 'Apple' == instance.name

    try:
        instance.set_name([])
    except TypeError:
        assert True


def test_set_code():
    instance = shp.Item()

    instance.set_code(11)
    assert 11 == instance.code

    instance.set_code(27)
    assert 27 == instance.code

    try:
        instance.set_code('one')
    except TypeError:
        assert True


def test_set_category():
    instance = shp.Item()

    instance.set_category('clothes')
    assert 'clothes' == instance.category

    instance.set_category('APPLE')
    assert 'APPLE' == instance.category

    try:
        instance.set_category(3432)
        assert False
    except TypeError:
        assert True


def test_set_destination():
    instance = shp.Item()

    instance.set_destination('Toronto')
    assert 'Toronto' == instance.destination

    instance.set_destination('USA')
    assert 'USA' == instance.destination

    try:
        instance.set_destination(342)
        assert False
    except TypeError:
        assert True


# Testing Shelf class

def test_shelf_init():
    instance = shp.Shelf(categories=['clothes'])
    assert instance == {'clothes': {}}

    instance = shp.Shelf(categories=['clothes', 'electronics', 'gloves'])
    assert instance == {'clothes': {}, 'electronics': {}, 'gloves': {}}


def test_insert():
    instance = shp.Shelf(categories=['clothes'])
    item = shp.Item(name='Jacket', code=3, category='clothes')

    instance.insert(item)
    assert instance['clothes'] == {3: item}

    instance = shp.Shelf(categories=['electronics'])
    instance.insert(item)
    assert instance == {'electronics': {}, 'clothes': {3: item}}


def test_force_insert():
    instance = shp.Shelf(categories=['random'])
    item = shp.Item(name='something', code=90, category='entities')

    instance.force_insert(category='random', item=item)

    assert instance == {'random': {item.code: item}}


def test_remove():
    instance = shp.Shelf(categories=['random'])
    item = shp.Item(name='something', code=12, category='entities')
    instance.insert(item)

    instance.remove(category='entities', code=item.code)
    assert instance == {'random': {}, 'entities': {}}

    instance = shp.Shelf(categories=['some category'])
    item = shp.Item(name='cucumber', code=31, category='some category')
    instance.insert(item)

    instance.remove(category='some category', code=item.code)
    assert instance == {'some category': {}}

    instance = shp.Shelf(categories=[None])
    item = shp.Item(name='cucumber', code=91, category=None)
    instance.insert(item)

    instance.remove(category=None, code=item.code)
    assert instance == {None: {}}


def test_retrieve():
    instance = shp.Shelf(categories=['random'])
    item = shp.Item(name='something', code=14, category='entities')
    instance.insert(item)

    assert instance.retrieve(category=item.category, code=item.code) == item

    instance = shp.Shelf(categories=[123])
    item = shp.Item(name='something', code=0, category=123)
    instance.insert(item)

    assert instance.retrieve(category=item.category, code=item.code) == item
