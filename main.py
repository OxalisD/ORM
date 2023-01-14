import sqlalchemy
from sqlalchemy import or_
import os
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale


login = 'postgres'
password =
DB = 'BooksSell'
DSN = f'postgresql://{login}:{password}@localhost:5432/{DB}'


def filling_tables(session):
    path_tests_data = os.path.join(os.getcwd(), "fixtures", "tests_data.json")
    with open(path_tests_data) as file:
        tests_data = json.load(file)

    data = []
    for model in tests_data:
        match model["model"]:
            case "publisher":
                data.append(Publisher(id=model["pk"], name=model["fields"]["name"]))
            case "book":
                data.append(
                    Book(id=model["pk"], title=model["fields"]["title"], id_publisher=model["fields"]["id_publisher"]))
            case "shop":
                data.append(Shop(id=model["pk"], name=model["fields"]["name"]))
            case "stock":
                data.append(
                    Stock(id=model["pk"], id_shop=model["fields"]["id_shop"], id_book=model["fields"]["id_book"],
                          count=model["fields"]["count"]))
            case "sale":
                data.append(Sale(id=model["pk"], price=model["fields"]["price"], date_sale=model["fields"]["date_sale"],
                                 count=model["fields"]["count"], id_stock=model["fields"]["id_stock"]))

    session.add_all(data)
    session.commit()

def get_sale(session, id=None, name=None):
    c = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Publisher, Book.id_publisher == Publisher.id) \
        .join(Stock, Stock.id_book == Book.id) \
        .join(Shop, Stock.id_shop == Shop.id) \
        .join(Sale, Sale.id_stock == Stock.id) \
        .filter(or_(Publisher.name == name, Publisher.id == id)) \
        .all()
    return c

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    for line in get_sale(session, id=input("Введите id автора: ")):
        print(f"{line[0]} | {line[1]} | {float(line[2])} | {str(line[3])}")
    create_tables(engine)
    filling_tables(session)

    session.close()
