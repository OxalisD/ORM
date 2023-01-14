import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

ProtoBase = declarative_base()


class Base(ProtoBase):
    __abstract__ = True
    id = sq.Column(sq.Integer, primary_key=True, unique=True, autoincrement=True)


class Publisher(Base):
    __tablename__ = "publisher"
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)


class Book(Base):
    __tablename__ = "book"
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", backref="books", uselist=False, lazy="joined")


class Shop(Base):
    __tablename__ = "shop"
    name = sq.Column(sq.String(length=40), nullable=False, unique=True)


class Stock(Base):
    __tablename__ = "stock"
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship("Book", backref="shops")
    shop = relationship("Shop", backref="books")


class Sale(Base):
    __tablename__ = "sale"
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship("Stock", backref="sales", uselist=False)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
