from operator import sub
import sqlite3
import requests
URL  = 'http://aexample.uz/api/'
class Database:
    def __init__(self, path_to_db="D:/Python/Bot/pizza_bot/test.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

#     def create_table_users(self):
#         sql = """
#         CREATE TABLE Users (
#             id int NOT NULL,
#             full_name varchar(255) NOT NULL,
#             username varchar(255),
#             telegram_id varchar(3),
#             PRIMARY KEY (id)
#             );
#           """
#         self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, full_name: str, username: str = None, telegram_id: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, full_name, username) VALUES(1, 'John', 'John@gmail.com')"
        data = {
        'full_name': full_name,
        'username': username,
        'telegram_id': telegram_id,
        }
        r = requests.post(url = f"{URL}user", data = data)
        # sql = """
        # INSERT INTO Users(id, full_name, username, telegram_id) VALUES(?, ?, ?, ?)
        # """
        # self.execute(sql, parameters=(id, full_name, username, telegram_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND full_name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def drop_table_users(self):
        self.execute("DROP TABLE Users", commit=True)

    # Productlarga bog'liq sql so'rovlar

    def get_categories(self):
        # return self.execute("SELECT * FROM categories", fetchall=True)
        PARAMS = {}
        req = requests.get(url = f"{URL}category", params = PARAMS)
        return req.json()
    
    def get_subcategories(self, category_id):
        # SQL_EXAMPLE = "SELECT * FROM subcategories where category=1"
        PARAMS = {}
        req = requests.get(url = f"{URL}subcategories/{category_id}", params = PARAMS)
        return req.json()
        # sql = f"SELECT * FROM subcategories where category_id={category_id}"
        # return self.execute(sql, fetchall=True)

    def get_subcategory(self, subcategory_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}subcategory/{subcategory_id}", params = PARAMS)
        return req.json()
        # sql = f"SELECT * FROM subcategories where id={subcategory_id}"
        # return self.execute(sql, fetchone=True)

    def get_user(self, user_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}user/{user_id}", params = PARAMS)
        return req.json()

    def get_products(self, subcategory_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}products/{subcategory_id}", params = PARAMS)
        return req.json()
        # sql = f"SELECT * FROM products where subcategory_id={subcategory_id}"
        # return self.execute(sql, fetchall=True)

    def get_product(self, item_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}product/{item_id}", params = PARAMS)
        return req.json()
        # sql = f"SELECT * FROM products where id={item_id}"
        # return self.execute(sql, fetchone=True)

    def add_to_cart(self, user_id: str, item_id: str, count: str):
        data = {
        'user':user_id,
        'product': item_id,
        'count': count,
        }
        r = requests.post(url = f"{URL}cart", data = data)
        # Response textni chop etish
        # sql = "INSERT INTO cart(user_id, product_id, count, price) VALUES(?, ?, ?, ?)"
        # self.execute(sql, parameters=(user_id, item_id, count), commit=True)

    
    def create_order(self, user_id: str, phone_number: str, name: str, total: str):
        data = {
        'user':user_id,
        'phone_number': phone_number,
        'name': name,
        'total': total,
        }
        r = requests.post(url = f"{URL}order", data = data)
        # Response textni chop etish
        # sql = "INSERT INTO order(user_id, phone_number, name, total) VALUES(?, ?, ?, ?)"
        # self.execute(sql, parameters=(user_id, name, total), commit=True)


    def get_order(self, user_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}order/last/{user_id}/", params = PARAMS)
        return req.json()

    def create_orderproduct(self, order_id: str, product: str, quantity: str):
        data = {
        'order':order_id,
        'product': product,
        'quantity': quantity,
        }
        r = requests.post(url = f"{URL}orderproduct", data = data)
        # Response textni chop etish
        # sql = "INSERT INTO order(user_id, phone_number, name, total) VALUES(?, ?, ?, ?)"
        # self.execute(sql, parameters=(user_id, name, total), commit=True)


    def get_cart(self, user_id):
        PARAMS = {}
        req = requests.get(url = f"{URL}cart/{user_id}/", params = PARAMS)
        return req.json()

        # sql = f"SELECT * FROM cart where user_id={user_id}"
        # return self.execute(sql, fetchall=True)

    def clear_cart(self, user_id: str):
        PARAMS = {}
        req = requests.get(url = f"{URL}clearcart/{user_id}/", params = PARAMS)
        return req.json()
        # sql = f"DELETE FROM cart WHERE user_id = {user_id}"
        # self.execute(sql, commit=True)

def logger(statement):
    pass
#     print(f"""
# _____________________________________________________        
# Executing: 
# {statement}
# _____________________________________________________
# """)