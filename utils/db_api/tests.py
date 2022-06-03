from unicodedata import category
from sqlite import Database
import requests


def test():
    db = Database(path_to_db='D:/Python/Bot/pizza_bot/test.db')
    # db.create_table_users()
    print("Ulanish...")
    # db.add_user(1, "One", "email", 'ru')
    URL  = 'http://aexample.uz/api/'
    PARAMS = {}
    req = requests.get(url = f"{URL}user/{143249567}", params = PARAMS)
    # req = requests.get(url = f"{URL}category", params = PARAMS)
    # users = db.select_all_users()
    # print(f"Barcha fodyalanuvchilar: {users}")
    # delete = db.drop_table_users()
    json = req.json()
    for js in json:
        print(f"{js['user_id']}")
    print("Ulandi")
    # items = db.get_products(1)
    # for item in items:
    #     print(item)
    # db.add_to_cart(2, 3)
    # cart_items = db.get_cart(143249567)
    # for item in cart_items:
    #     product = db.get_product(item[3])
    #     nom = db.get_subcategory(product[5])
    #     print(f"Maxsulot: {nom[1]} {product[1]}, Soni: {item[1]} ta, Narxi: {item[2]} so'm\n")
    # categor = db.get_subcategories(1)
    # print(f"Subcategory: {categor}")
    # prod = db.get_product(2)
    # print(f"Product: {prod}")
    # print(f"Barcha categoriyalar: {categories}")
    # user = db.select_user(Name="John", id=5)
    # print(f"Bitta foydalanuvchini ko'rish: {user}")



test()