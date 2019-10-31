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

    shp.Item.all_codes = []


def test_insert():
    instance = shp.Shelf(categories=['clothes'])
    item = shp.Item(name='Jacket', code=3, category='clothes')

    instance.insert(item)
    assert instance['clothes'] == {3: item}

    instance = shp.Shelf(categories=['electronics'])
    instance.insert(item)
    assert instance == {'electronics': {}, 'clothes': {3: item}}

    shp.Item.all_codes = []


def test_force_insert():
    instance = shp.Shelf(categories=['random'])
    item = shp.Item(name='something', code=90, category='entities')

    instance.force_insert(category='random', item=item)

    assert instance == {'random': {item.code: item}}

    shp.Item.all_codes = []


def test_shelf_remove():
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

    shp.Item.all_codes = []


def test_retrieve():
    instance = shp.Shelf(categories=['random'])
    item = shp.Item(name='something', code=14, category='entities')
    instance.insert(item)

    assert instance.retrieve(category=item.category, code=item.code) == item

    instance = shp.Shelf(categories=[123])
    item = shp.Item(name='something', code=0, category=123)
    instance.insert(item)

    assert instance.retrieve(category=item.category, code=item.code) == item

    shp.Item.all_codes = []


# Test Bin Class

def test_send_bin():
    shipment = shp.Bin('in', contents=[shp.Item()], destination='Toronto', number=87)
    truck = shp.Truck(destination='Toronto')

    shipment.send_bin(truck)
    assert truck.contents[0] == shipment

    shipment = shp.Bin('in', contents=[shp.Item(code=14)], destination='random', number=87)
    truck = shp.Truck(destination='random')

    shipment.send_bin(truck)
    assert truck.contents[0] == shipment

    shipment = shp.Bin('in', contents=[shp.Item(code=1331)], destination='random', number=87)
    truck = shp.Truck(destination='Toronto')

    try:
        shipment.send_bin(truck)
        assert False
    except shp.ShipmentError:
        assert True

    shp.Item.all_codes = []


def test_item_count():
    shipment = shp.Bin('in', contents=[shp.Item(code=1331),
                                       shp.Item(code=12345),
                                       shp.Item(code=678)],
                       destination='random',
                       number=8)
    assert shipment.item_count() == 3

    shipment = shp.Bin('out', contents=[shp.Item()], destination='someplace', number=8)
    assert shipment.item_count() == 1

    shp.Item.all_codes = []


def test_add():
    shipment = shp.Bin('out', contents=[], destination='someplace', number=8)
    item = shp.Item()

    shipment.add(item)
    assert shipment.contents == [item]

    shipment = shp.Bin('in', contents=[shp.Item(code=1331),
                                       shp.Item(code=12345),
                                       shp.Item(code=678)],
                       destination='random',
                       number=8)

    item = shp.Item(code=43654)

    shipment.add(item)
    assert shipment.contents[-1] == item

    shp.Item.all_codes = []


def test_bin_remove():
    item = shp.Item(code=43654)
    shipment = shp.Bin('in', contents=[item],
                       destination='random',
                       number=8)
    shipment.remove(item)
    assert shipment.contents == []

    item1, item2, item3 = shp.Item(code=57), shp.Item(code=900), shp.Item(code=84)
    shipment = shp.Bin('in', contents=[item1, item2, item3],
                       destination='random',
                       number=8)
    shipment.remove(item2)
    assert shipment.contents == [item1, item3]

    shp.Item.all_codes = []


def test_get_item():
    item = shp.Item(code=43654)
    shipment = shp.Bin('in', contents=[item],
                       destination='random',
                       number=8)
    assert shipment.get_item(item.code) == item

    item1, item2, item3 = shp.Item(code=57), shp.Item(code=89), shp.Item(code=84)
    shipment = shp.Bin('in', contents=[item1, item2, item3],
                       destination='random',
                       number=8)

    assert shipment.get_item(57) == item1
    assert shipment.get_item(780) == -1

    shp.Item.all_codes = []


# Test Truck Class

def test_is_delivered():
    item = shp.Item(code=43654)
    shipment = shp.Bin('in', contents=[item],
                       destination='Toronto',
                       number=8)

    truck = shp.Truck(destination='Toronto')
    truck.contents = [shipment]

    truck.deliver()

    assert truck.contents == []
    assert truck.is_delivered() is True

    item, item2 = shp.Item(code=45), shp.Item(code=90)
    shipment = shp.Bin('in', contents=[item, item2],
                       destination='Toronto',
                       number=8)

    truck = shp.Truck(destination='Toronto')
    truck.contents = [shipment]

    truck.deliver()

    assert truck.contents == []
    assert truck.is_delivered() is True

    shp.Item.all_codes = []


def test_deliver():
    item = shp.Item(code=43654)
    shipment = shp.Bin('in', contents=[item],
                       destination='Toronto',
                       number=8)

    truck = shp.Truck(destination='Toronto')
    truck.contents = [shipment]

    truck.deliver()
    assert truck.contents == []

    item, item2 = shp.Item(code=45), shp.Item(code=90)
    shipment = shp.Bin('in', contents=[item, item2],
                       destination='Toronto',
                       number=8)

    truck = shp.Truck(destination='Toronto')
    truck.contents = [shipment]

    truck.deliver()
    assert truck.contents == []

    shp.Item.all_codes = []


def test_load_bin():
    item, item2 = shp.Item(code=45), shp.Item(code=90)
    shipment = shp.Bin('in', contents=[item, item2],
                       destination='Toronto',
                       number=8)

    truck = shp.Truck(destination='Toronto')
    truck.load_bin(shipment)
    assert truck.contents == [shipment]

    item = shp.Item()
    shipment = shp.Bin('in', contents=[item], destination='Calgary', number=8)

    try:
        truck.load_bin(shipment)
        assert False
    except shp.ShipmentError:
        assert True
