from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
menu_cd = CallbackData("show_menu", "lang", "level", "category", "subcategory", "item_id", "one", "two")
buy_item = CallbackData("buy", "item_id")


# Quyidagi funksiya yordamida menyudagi har bir element uchun calbback data yaratib olinadi
# Agar mahsulot kategoriyasi, ost-kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(level, lang, category="0", subcategory="0", item_id="0", one = "0", two = "0"):
    return menu_cd.new(
        level=level, lang=lang, category=category, subcategory=subcategory, item_id=item_id, one=one, two=two
    )


# Bizning menu 3 qavat (LEVEL) dan iborat
# 0 - Kategoriyalar
# 1 - Ost-kategoriyalar
# 2 - Mahsulotlar
# 3 - Yagona mahsulot
# 4 - Sonini tanlash


# Kategoriyalar uchun keyboardyasab olamiz
async def categories_keyboard(lang):
    # Eng yuqori 0-qavat ekanini ko'rsatamiz
    CURRENT_LEVEL = 0

    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=2)

    # Bazadagi barcha kategoriyalarni olamiz
    categories = db.get_categories()
    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for category in categories:
        button_text = ''
        # Tugma matnini yasab olamiz
        if lang == 'ru':
            button_text = f"{category['title']}"
        elif lang == 'uz':
            button_text = f"{category['title_uz']}"
        elif lang == 'cn':
            button_text = f"{category['title_cn']}"
        # print(category)

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, lang=lang, category=category['id']
        )
        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Keyboardni qaytaramiz
    return markup


# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(lang, category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = db.get_subcategories(category)
    for subcategory in subcategories:
        button_text = ''
        cancel = ''
        # Tugma matnini yasaymiz
        if lang == 'ru':
            button_text = f"{subcategory['title']}"
            cancel = "⬅️ Назад"
        elif lang == 'uz':
            button_text = f"{subcategory['title_uz']}"
            cancel = "⬅️ Orqaga"
        elif lang == 'cn':
            button_text = f"{subcategory['title_cn']}"
            cancel = "⬅️ 后退"
        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            lang=lang,
            subcategory=subcategory['id'],
            one=0,
            two=10
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasini yasaymiz (yuqori qavatga qaytamiz)
    markup.row(
        InlineKeyboardButton(
            text=cancel, callback_data=make_callback_data(level=CURRENT_LEVEL - 1, lang=lang)
        )
    )
    return markup


# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz
async def items_keyboard(lang, subcategory, one, two):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz 
    items = db.get_products(subcategory)[one:two]
    count = len(db.get_products(subcategory))
    # print(db.get_subcategories(subcategory)[0]['category'])
    category_id = db.get_subcategory(subcategory)['category']
    # print(f"{category_id}")
    oldingi = ''
    keyingi = ''
    button_text = ''
    cancel = ''
    for item in items:
        # Tugma matnini yasaymiz
        
        if lang == 'ru':
            button_text = f"{item['title']}"
            keyingi = "следующий ⏭"
            oldingi = "⏮ предыдущий"
            cancel = "⬅️Назад"
        elif lang == 'uz':
            button_text = f"{item['title_uz']}"
            keyingi = "Keyingi ⏭"
            oldingi = "⏮ Avvalgi"
            cancel = "⬅️Orqaga"
        elif lang == 'cn':
            button_text = f"{item['title_uz']}"
            keyingi = " ⏭下一个"
            oldingi = "⏮ Avvalgi"
            cancel = "⬅️ 后退"
        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            lang=lang,
            item_id=item['id'],
            one = one,
            two = two
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    
    next = make_callback_data(
            level=CURRENT_LEVEL,
            lang=lang,
            subcategory=subcategory,
            one = two,
            two = two + 10
    )
    prew = make_callback_data(
        level=CURRENT_LEVEL,
        lang=lang,
        subcategory=subcategory,
        two = one,
        one = one-10
    )
    if one > 0 and two < count:
        markup.add(
        InlineKeyboardButton(text=keyingi, callback_data = next),
        InlineKeyboardButton(text=oldingi, callback_data = prew)
        )
    elif two >= count and count > 10:
        markup.insert(
        InlineKeyboardButton(text=oldingi, callback_data = prew)
        )
    elif count > 10:
        markup.insert(
        InlineKeyboardButton(text=keyingi, callback_data = next)
        )
    
        

    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text=cancel,
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, lang=lang, category=category_id
            ),
        )
    )
    return markup


# Berilgan mahsulot uchun Xarid qilish va Ortga yozuvlarini chiqaruvchi tugma keyboard
def item_keyboard(lang, item_id, one, two):
    item = db.get_product(item_id)
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    cancel = ''
    cart = ''
    if lang == 'ru':
        cart = "🛒 Добавить в корзину"
        cancel = "⬅️Назад"
    elif lang == 'uz':
        cart = "🛒 Savatga qo'shish"
        cancel = "⬅️Orqaga"
    elif lang == 'cn':
        cart = "🛒 加入购物篮"
        cancel = "⬅️后退"
    callback_data = make_callback_data(
            lang=lang,
            level=CURRENT_LEVEL + 1,
            item_id=item_id
        )
    markup.row(
        InlineKeyboardButton(
            text=cart, callback_data=callback_data
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=cancel,
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, lang=lang,  subcategory=item['subcategory'], one=one, two=two
            ),
        )
    )
    return markup 


def count_keyboard(lang, item_id):
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup(row_width=3)
    cancel = ''
    if lang == 'ru':
        cancel = "⬅️Назад"
    elif lang == 'uz':
        cancel = "⬅️Orqaga"
    elif lang == 'cn':
        cancel = "⬅️后退"
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
    ),
    markup.row(
        InlineKeyboardButton(text=cancel, callback_data=make_callback_data(level=CURRENT_LEVEL - 1, lang=lang, item_id=item_id),)
        )
    return markup


def showcart(lang):
    markup = InlineKeyboardMarkup(one_time_keyboard=True)
    text = ''
    text2 = ''
    if lang == 'ru':
        text="Заказать"
        text2="Очистить"
    elif lang == 'uz':
        text="Buyurtma berish"
        text2="Tozalash"
    elif lang == 'cn':
        text="订购"
        text2="取消"
    markup.row(
        InlineKeyboardButton(text=text, callback_data="buy"),
        InlineKeyboardButton(text=text2, callback_data="clear"),
    )
    return markup


def confirm(lang):
    markup = InlineKeyboardMarkup(one_time_keyboard=True)
    text = ''
    text2 = ''
    if lang == 'ru':
        text="Подтвердить"
        text2="Не подтверждать"
    elif lang == 'uz':
        text="Tasdiqlash"
        text2="Rad etish"
    elif lang == 'cn':
        text="确认"
        text2="不确认"
    markup.row(
        InlineKeyboardButton(text=text, callback_data="yes"),
        InlineKeyboardButton(text=text2, callback_data="no"),
    )
    return markup


def buy_item(lang):
    markup = InlineKeyboardMarkup()
    text = ''
    text2 = ''
    if lang == 'ru':
        text="Наличные"
        text2="Оплата по карте"
    elif lang == 'uz':
        text="Naqd"
        text2="Karta orqali"
    elif lang == 'cn':
        text="现金付款"
        text2="银行卡转账"
    markup.row(
        InlineKeyboardButton(text=text, callback_data="cash"),
        InlineKeyboardButton(text=text2, callback_data="by_cart"), #url="https://indoor.click.uz/pay?id=048869&t=0"),
    )
    return markup


def pay(lang):
    markup = InlineKeyboardMarkup()
    text = ''
    text2 = ''
    if lang == 'ru':
        text="Оплатить"
    elif lang == 'uz':
        text="To'lash"
    elif lang == 'cn':
        text="To'lash"
    markup.row(
        InlineKeyboardButton(text=text, callback_data="by_cart", url="https://indoor.click.uz/pay?id=048869&t=0"),
        )
    return markup


def change_lang():
    markup = InlineKeyboardMarkup(one_time_keyboard=True)
    markup.row(
        InlineKeyboardButton(text="UZ 🇺🇿", callback_data="UZB"),
        InlineKeyboardButton(text="RU 🇷🇺", callback_data="RUS"),
        
    )
    return markup

#InlineKeyboardButton(text="CH 🇨🇳", callback_data="CHINA"),