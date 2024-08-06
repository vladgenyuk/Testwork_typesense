from project.typesense_utils import create_client

client = create_client()

schema = {
    'name': 'products',
    'fields': [
        {
            'name': 'uuid',
            'type': 'string',
            'facet': False,
            'optional': False,
            'index': True,
            'comment': 'id товара в нашей бд'
        },
        {
            'name': 'product_id',
            'type': 'string',
            'facet': False,
            'optional': False,
            'index': True,
            'comment': 'id товара в маркетплейсе'
        },
        {
            'name': 'title',
            'type': 'string',
            'facet': False,
            'optional': False,
            'index': True,
            'comment': 'название товара',
            'sort': True,
        },
        {
            'name': 'description',
            'type': 'string',
            'facet': False,
            'optional': True,
            'index': True,
            'comment': 'описание товара',
            'sort': True,
        },
        {
            'name': 'price_before_discounts',
            'type': 'float',
            'facet': False,
            'optional': False,
            'index': True,
            'comment': 'цена товара'
        },
        {
            'name': 'discount',
            'type': 'float',
            'facet': False,
            'optional': True,
            'index': True,
            'comment': 'скидка на товар'
        },
        {
            'name': 'category_remaining',
            'type': 'string',
            'facet': True,
            'optional': True,
            'index': True,
            'comment': 'Остаток категории товара. Например, для товара, '
            'находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и '
            'игры/Игровые консоли, в это поле запишется "Игровая консоль/Игровые консоли и игры/Игровые консоли".'
        },
        {
            'name': 'barcode',
            'type': 'string',
            'facet': False,
            'optional': True,
            'index': True,
            'comment': 'Штрихкод'
        }
    ],
    'default_sorting_field': 'price_before_discounts'
}

try:
    client.collections.create(schema)
    print("Collection created successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
