# Створення бази даних та сесії
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_creation import Client, Product, Sale, Warehouse, db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Видалення всіх записів з таблиць
session.execute(Sale.__table__.delete())
session.execute(Product.__table__.delete())
session.execute(Client.__table__.delete())
session.execute(Warehouse.__table__.delete())

session.commit()

# Скидання лічильників id значень
# session.execute(
#     f'DELETE FROM sqlite_sequence WHERE name="{Warehouse.__tablename__}"')
# session.execute(
#     f'DELETE FROM sqlite_sequence WHERE name="{Product.__tablename__}"')
# session.execute(
#     f'DELETE FROM sqlite_sequence WHERE name="{Client.__tablename__}"')
# session.execute(
#     f'DELETE FROM sqlite_sequence WHERE name="{Sale.__tablename__}"')

session.commit()
session.close()
