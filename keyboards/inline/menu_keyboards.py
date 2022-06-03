from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")


# Quyidagi funksiya yordamida menyudagi har bir element uchun calbback data yaratib olinadi
# Agar mahsulot kategoriyasi, ost-kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(
        level=level, category=category, subcategory=subcategory, item_id=item_id
    )


# Bizning menu 3 qavat (LEVEL) dan iborat
# 0 - Kategoriyalar
# 1 - Ost-kategoriyalar
# 2 - Mahsulotlar
# 3 - Yagona mahsulot
# 4 - Sonini tanlash


# Kategoriyalar uchun keyboardyasab olamiz
async def categories_keyboard():
    # Eng yuqori 0-qavat ekanini ko'rsatamiz
    CURRENT_LEVEL = 0

    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=2)

    # Bazadagi barcha kategoriyalarni olamiz
    categories = db.get_categories()
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for category in categories:

        # Tugma matnini yasab olamiz
        button_text = f"{category['title']} "
        # print(category)

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=category['id']
        )

        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Keyboardni qaytaramiz
    return markup


# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = db.get_subcategories(category)
    for subcategory in subcategories:
        

        # Tugma matnini yasaymiz
        button_text = f"{subcategory['title']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            subcategory=subcategory['id'],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasini yasaymiz (yuqori qavatga qaytamiz)
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz
async def items_keyboard(subcategory):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=2)

    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz
    items = db.get_products(subcategory)
    # print(db.get_subcategories(subcategory)[0]['category'])
    category_id = db.get_subcategories(subcategory)[0]['category']
    for item in items:
        # Tugma matnini yasaymiz
        button_text = f"{item['title']} - {item['price']} so'm"
        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            item_id=item['id'],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category_id
            ),
        )
    )
    return markup


# Berilgan mahsulot uchun Xarid qilish va Ortga yozuvlarini chiqaruvchi tugma keyboard
def item_keyboard(item_id):
    item = db.get_product(item_id)
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            item_id=item_id
        )
    markup.row(
        InlineKeyboardButton(
            text=f"🛒 Savatga qo'shish", callback_data=callback_data
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,  subcategory=item['subcategory']
            ),
        )
    )
    return markup


def count_keyboard(item_id):
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
            InlineKeyboardButton(text="1", callback_data=f"number 1 item_id  {item_id}"),
            InlineKeyboardButton(text="2", callback_data=f"number 2 item_id  {item_id}"),
            InlineKeyboardButton(text="3", callback_data=f"number 3 item_id  {item_id}"),
    ),
    markup.row(    
            InlineKeyboardButton(text="4", callback_data=f"number 4 item_id  {item_id}"),
            InlineKeyboardButton(text="5", callback_data=f"number 5 item_id  {item_id}"),
            InlineKeyboardButton(text="6", callback_data=f"number 6 item_id  {item_id}"),
    ),
    markup.row(    
            InlineKeyboardButton(text="7", callback_data=f"number 7 item_id  {item_id}"),
            InlineKeyboardButton(text="8", callback_data=f"number 8 item_id  {item_id}"),
            InlineKeyboardButton(text="9", callback_data=f"number 9 item_id  {item_id}"),
    )
    return markup


def showcart():
    markup = InlineKeyboardMarkup(one_time_keyboard=True)
    markup.row(
        InlineKeyboardButton(text="Sotib olish", callback_data="buy"),
        InlineKeyboardButton(text="Tozalash", callback_data="clear"),
    )
    return markup


def confirm():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Tasdiqlayman", callback_data="yes"),
        InlineKeyboardButton(text="Yo'q", callback_data="no"),
    )
    return markup


def buy_item():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Naqd", callback_data="cash"),
        InlineKeyboardButton(text="Karta orqali", callback_data="by_cart"),
    )
    return markup
