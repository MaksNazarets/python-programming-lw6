from sqlalchemy import create_engine
from db_creation import Client, Product, Sale, Warehouse, db_url
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

warehouses = [Warehouse(address='Адреса 1', warehouse_manager='Менеджер 1', phone='Телефон 1'),
              Warehouse(address='Адреса 2',
                        warehouse_manager='Менеджер 2', phone='Телефон 2'),
              Warehouse(address='Адреса 3', warehouse_manager='Менеджер 3', phone='Телефон 3')]

clients = [Client(client_name='Клієнт 1', client_address='Адреса 1',
                  client_phone='Телефон 1'),
           Client(client_name='Клієнт 2', client_address='Адреса 2',
                  client_phone='Телефон 2'),
           Client(client_name='Клієнт 3', client_address='Адреса 3',
                  client_phone='Телефон 3'),
           Client(client_name='Клієнт 4', client_address='Адреса 4',
                  client_phone='Телефон 4'),
           Client(client_name='Клієнт 5', client_address='Адреса 5',
                  client_phone='Телефон 5'),
           Client(client_name='Клієнт 6', client_address='Адреса 6',
                  client_phone='Телефон 6'),
           Client(client_name='Клієнт 7', client_address='Адреса 7',
                  client_phone='Телефон 7'),
           ]

products = [
    Product(type='жіночий', clothing_name='Назва 1', manufacturer='Виробник 1',
            warehouse_id=1, quantity_in_stock=10, price=20.0),
    Product(type='чоловічий', clothing_name='Назва 2', manufacturer='Виробник 2',
            warehouse_id=2, quantity_in_stock=15, price=30.0),
    Product(type='жіночий', clothing_name='Назва 3', manufacturer='Виробник 3',
            warehouse_id=1, quantity_in_stock=5, price=15.0),
    Product(type='жіночий', clothing_name='Назва 4', manufacturer='Виробник 4',
            warehouse_id=3, quantity_in_stock=8, price=25.0),
    Product(type='дитячий', clothing_name='Назва 5', manufacturer='Виробник 5',
            warehouse_id=2, quantity_in_stock=12, price=22.0),
    Product(type='чоловічий', clothing_name='Назва 6', manufacturer='Виробник 6',
            warehouse_id=1, quantity_in_stock=18, price=35.0),
    Product(type='чоловічий', clothing_name='Назва 7', manufacturer='Виробник 7',
            warehouse_id=3, quantity_in_stock=20, price=18.0),
    Product(type='жіночий', clothing_name='Назва 8', manufacturer='Виробник 3',
            warehouse_id=1, quantity_in_stock=14, price=28.0),
    Product(type='дитячий', clothing_name='Назва 9', manufacturer='Виробник 1',
            warehouse_id=2, quantity_in_stock=20, price=40.0),
    Product(type='дитячий', clothing_name='Назва 10', manufacturer='Виробник 6',
            warehouse_id=3, quantity_in_stock=25, price=45.0),
    Product(type='жіночий', clothing_name='Назва 11', manufacturer='Виробник 1',
            warehouse_id=1, quantity_in_stock=30, price=50.0),
    Product(type='чоловічий', clothing_name='Назва 12', manufacturer='Виробник 3',
            warehouse_id=2, quantity_in_stock=5, price=10.0),
    Product(type='дитячий', clothing_name='Назва 13', manufacturer='Виробник 5',
            warehouse_id=3, quantity_in_stock=13, price=26.0),
    Product(type='жіночий', clothing_name='Назва 14', manufacturer='Виробник 3',
            warehouse_id=1, quantity_in_stock=17, price=34.0),
    Product(type='жіночий', clothing_name='Назва 15', manufacturer='Виробник 6',
            warehouse_id=2, quantity_in_stock=22, price=44.0),
    Product(type='жіночий', clothing_name='Назва 16', manufacturer='Виробник 5',
            warehouse_id=3, quantity_in_stock=8, price=16.0),
    Product(type='дитячий', clothing_name='Назва 17', manufacturer='Виробник 6',
            warehouse_id=1, quantity_in_stock=11, price=33.0),
]

sales = [
    Sale(client_id=1, product_id=1, quantity_purchased=5, discount=0.1),
    Sale(client_id=2, product_id=2, quantity_purchased=3, discount=0.05),
    Sale(client_id=3, product_id=3, quantity_purchased=8, discount=0.15),
    Sale(client_id=4, product_id=4, quantity_purchased=2, discount=0.02),
    Sale(client_id=5, product_id=5, quantity_purchased=10, discount=0.2),
    Sale(client_id=6, product_id=6, quantity_purchased=4, discount=0.08),
    Sale(client_id=7, product_id=7, quantity_purchased=7, discount=0.12),
    Sale(client_id=6, product_id=8, quantity_purchased=6, discount=0.18),
    Sale(client_id=4, product_id=9, quantity_purchased=3, discount=0.09),
    Sale(client_id=1, product_id=10, quantity_purchased=15, discount=0.25),
    Sale(client_id=4, product_id=11, quantity_purchased=2, discount=0.03),
    Sale(client_id=5, product_id=12, quantity_purchased=9, discount=0.1),
    Sale(client_id=6, product_id=6, quantity_purchased=4, discount=0.08),
    Sale(client_id=1, product_id=1, quantity_purchased=5, discount=0.1),
    Sale(client_id=7, product_id=15, quantity_purchased=18, discount=0.2),
    Sale(client_id=7, product_id=7, quantity_purchased=5, discount=0.12),
    Sale(client_id=4, product_id=4, quantity_purchased=2, discount=0.02),
    Sale(client_id=3, product_id=1, quantity_purchased=8, discount=0.15),
    Sale(client_id=1, product_id=2, quantity_purchased=2, discount=0.02),
    Sale(client_id=7, product_id=3, quantity_purchased=10, discount=0.2),
    Sale(client_id=2, product_id=4, quantity_purchased=4, discount=0.08),
    Sale(client_id=2, product_id=5, quantity_purchased=7, discount=0.12),
]


session.add_all(warehouses)
session.add_all(clients)
session.commit()

session.add_all(products)
session.commit()

session.add_all(sales)
session.commit()
session.close()

print('Додано ✓')
