from msilib import Table
from prettytable import PrettyTable
from sqlalchemy import Float, MetaData, create_engine, func
from sqlalchemy.orm import sessionmaker
from db_creation import Client, Product, Sale, Warehouse, db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def print_table_structure(table_class):
    table_name = table_class.__tablename__
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"\nСтруктура таблиці '{table_name}':")
        for column in table.columns:
            print(f"{column.name} - {column.type}")
    else:
        print(f"\nТаблиці '{table_name}' не існує у базі даних.")


def show_all_tables():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    for table_name in metadata.tables.keys():
        table = metadata.tables[table_name]

        results = session.query(table).all()

        if results:
            print(f"\nДані в таблиці '{table_name}':")
            table_data = PrettyTable()
            table_data.field_names = table.columns.keys()

            for row in results:
                table_data.add_row(row)

            print(table_data)
        else:
            print(f"\nВ таблиці '{table_name}' немає даних.")


def show_sales():
    display_purchases_query = (
        session.query(
            Sale.sale_date.label("Дата покупки"),
            Product.clothing_name.label("Назва товару"),
            Client.client_name.label("Клієнт"),
            Sale.quantity_purchased.label("К-сть куплено"),
            Product.price.label("Ціна")
        )
        .join(Product, Sale.product_id == Product.product_id)
        .join(Client, Sale.client_id == Client.client_id)
        .order_by(Client.client_name)
    )

    results = display_purchases_query.all()

    table = PrettyTable()
    table.field_names = ["Дата покупки", "Назва товару",
                         "Клієнт", "К-сть куплено", "Ціна"]
    table.align["Дата покупки"] = "l"
    table.align["Назва товару"] = "l"
    table.align["Клієнт"] = "l"
    table.align["К-сть куплено"] = "l"
    table.align["Ціна"] = "l"

    for row in results:
        table.add_row(row)

    print("Покупки:")
    print(table)


def show_products_by_type():
    type_translation = {
        "ч": "чоловічий",
        "ж": "жіночий",
        "д": "дитячий"
    }

    type_name = input(
        "\nВведіть назву типу одягу (ч - чоловічий, \n\tж - жіночий, \n\tд - дитячий): ")

    while type_name not in ['ч', 'ж', 'д']:
        print('Такого типу не існує')
        type_name = input(
            "\nВведіть назву типу одягу (ч - чоловічий, \n\tж - жіночий, \n\tд - дитячий): ")

    type_name = type_translation[type_name]

    results = (
        session.query(
            Product.clothing_name.label("Назва товару"),
            Product.manufacturer.label("Виробник"),
            Product.price.label("Ціна"),
            Product.quantity_in_stock.label("К-сть в наявності")
        )
        .filter_by(type=type_name)
        .all()
    )

    if not results:
        print(f"Не знайдено жодного одягу із типом \"{type_name}\"")
    else:
        table = PrettyTable()
        table.field_names = ["Назва товару", "Виробник",
                             "Ціна", "К-сть в наявності"]
        table.align["Назва товару"] = "l"
        table.align["Виробник"] = "l"
        table.align["Ціна"] = "l"
        table.align["К-сть в наявності"] = "l"

        for row in results:
            table.add_row(row)

        print(f"\nОдяг типу \"{type_name}\":")
        print(table)

        session.close()


def show_purchase_count_by_client():
    purchase_count_query = (
        session.query(
            Client.client_name.label("Клієнт"),
            func.count().label("Кількість покупок")
        )
        .join(Sale, Sale.client_id == Client.client_id)
        .group_by(Client.client_name)
        .order_by(Client.client_name)
    )

    results = purchase_count_query.all()

    table = PrettyTable()
    table.field_names = ["Клієнт", "Кількість покупок"]
    table.align["Клієнт"] = "l"
    table.align["Кількість покупок"] = "l"

    for row in results:
        table.add_row(row)

    print("Кількість покупок за кожним клієнтом:")
    print(table)

    session.close()


def show_purchase_cost():
    purchase_cost_query = (
        session.query(
            Sale.sale_id.label("Номер покупки"),
            Product.clothing_name.label("Назва товару"),
            Sale.quantity_purchased.label("К-сть куплено"),
            Product.price.label("Ціна за одиницю"),
            Sale.discount.label("Знижка"),
            func.cast((Sale.quantity_purchased * Product.price),
                      Float(2)).label("Вартість без знижки"),
            func.cast((Sale.quantity_purchased * Product.price *
                      (1 - Sale.discount)), Float(2)).label("Вартість зі знижкою")
        )
        .join(Product, Sale.product_id == Product.product_id)
        .order_by(Sale.sale_id)
    )

    results = purchase_cost_query.all()

    table = PrettyTable()
    table.field_names = ["Номер покупки", "Назва товару", "К-сть куплено",
                         "Ціна за одиницю", "Знижка", "Вартість без знижки", "Вартість зі знижкою"]
    table.align["Номер покупки"] = "l"
    table.align["Назва товару"] = "l"
    table.align["К-сть куплено"] = "l"
    table.align["Ціна за одиницю"] = "l"
    table.align["Знижка"] = "l"
    table.align["без знижки"] = "l"
    table.align["Вартість зі знижкою"] = "l"

    for row in results:
        table.add_row(row)

    print("Вартість покупок з урахуванням знижки:")
    print(table)
    session.close()


def show_total_money_spent_by_client():
    total_money_spent_query = (
        session.query(
            Client.client_name.label("Клієнт"),
            func.cast(func.sum(Sale.quantity_purchased * Product.price *
                      (1 - Sale.discount)), Float(2)).label("Загальна сума витрат")

        )
        .join(Sale, Sale.client_id == Client.client_id)
        .join(Product, Sale.product_id == Product.product_id)
        .group_by(Client.client_name)
        .order_by(Client.client_name)
    )

    results = total_money_spent_query.all()

    table = PrettyTable()
    table.field_names = ["Клієнт", "Загальна сума витрат"]
    table.align["Клієнт"] = "l"
    table.align["Загальна сума витрат"] = "l"

    for row in results:
        table.add_row(row)

    print("Загальна сума витрат кожного клієнта:")
    print(table)


def show_clothing_quantity_by_warehouse():
    cross_tab_query = (
        session.query(
            Warehouse.address.label("Адреса складу"),
            Product.clothing_name.label("Назва одягу"),
            func.sum(Product.quantity_in_stock).label("Кількість")
        )
        .join(Product, Product.warehouse_id == Warehouse.warehouse_id)
        .group_by(Warehouse.address, Product.clothing_name)
        .order_by(Warehouse.address, Product.clothing_name)
    )

    results = cross_tab_query.all()

    table = PrettyTable()
    table.field_names = ["Адреса складу", "Назва одягу", "Кількість"]
    table.align["Адреса складу"] = "l"
    table.align["Назва одягу"] = "l"
    table.align["Кількість"] = "l"

    last_warehouse = None

    for row in results:
        if row[0] == last_warehouse:
            r = list(row)
            r[0] = ''
            table.add_row(r)
            continue

        table.add_row(row)
        last_warehouse = row[0]

    print("Кількість кожного виду одягу на кожному складі:")
    print(table)


if __name__ == "__main__":
    print_table_structure(Warehouse)
    print_table_structure(Product)
    print_table_structure(Client)
    print_table_structure(Sale)

    show_all_tables()
    print()

    show_sales()
    print()

    show_products_by_type()
    print()

    show_purchase_count_by_client()
    print()

    show_purchase_cost()
    print()

    show_total_money_spent_by_client()
    print()

    show_clothing_quantity_by_warehouse()

session.close()
