from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

db_url = "postgresql://maks:my_pass@localhost:5435/clothing_store"
engine = create_engine(db_url)

Base = declarative_base()


class Warehouse(Base):
    __tablename__ = 'warehouse'
    warehouse_id = Column(Integer, primary_key=True)
    address = Column(String)
    warehouse_manager = Column(String)
    phone = Column(String)


class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    type = Column(String)
    clothing_name = Column(String)
    manufacturer = Column(String)
    warehouse_id = Column(Integer, ForeignKey('warehouse.warehouse_id'))
    quantity_in_stock = Column(Integer)
    price = Column(Float)


class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    client_name = Column(String)
    client_address = Column(String)
    client_phone = Column(String)


class Sale(Base):
    __tablename__ = 'sale'
    sale_id = Column(Integer, primary_key=True)
    sale_date = Column(Date, default=func.current_date())
    client_id = Column(Integer, ForeignKey('client.client_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    quantity_purchased = Column(Integer)
    discount = Column(Float)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

engine.dispose()
