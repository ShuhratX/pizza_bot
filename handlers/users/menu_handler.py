from typing import Union
from keyboards.default.show_menu import contact, location, menu
from aiogram import types
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, ReplyKeyboardRemove
from data.config import ADMINS
from geopy.geocoders import Nominatim

from keyboards.inline.menu_keyboards import (
    menu_cd,
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard,
    item_keyboard,
    count_keyboard,
    showcart, 
    buy_item,
    confirm
)

from loader import dp, db, bot


# Bosh menyu matni uchun handler
@dp.message_handler(text="Bosh menyu")
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    await list_categories(message)


# Kategoriyalarni qaytaruvchi funksiya. Callback query yoki Message qabul qilishi ham mumkin.
# **kwargs yordamida esa boshqa parametrlarni ham qabul qiladi: (category, subcategory, item_id)
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Keyboardni chaqiramiz
    markup = await categories_keyboard()

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        await message.answer("Bo'lim tanlang", reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Ost-kategoriyalarni qaytaruvchi funksiya
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)

    # Xabar matnini o'zgartiramiz va keyboardni yuboramiz
    await callback.message.edit_reply_markup(markup)


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, subcategory, **kwargs):
    markup = await items_keyboard(subcategory)

    await callback.message.edit_text(text="Mahsulot tanlang", reply_markup=markup)


# Biror mahsulot uchun Xarid qilish tugmasini yuboruvchi funksiya
async def show_item(callback: CallbackQuery, item_id, **kwargs):
    markup = item_keyboard(item_id)

    # Mahsulot haqida ma'lumotni bazadan olamiz
    item = db.get_product(item_id)

    if item['image']:
        text = f"<a href=\"{item['image']}\">{item['title']}</a>\n\n"
    else:
        text = f"{item['title']}\n\n"
    text += f"Narxi: {item['price']}so'm\n{item['structure']}"

    await callback.message.edit_text(text=text, reply_markup=markup)


async def send_count(callback: CallbackQuery, item_id, **kwargs):
    markup = count_keyboard(item_id)
    await callback.message.edit_text(text = "Mahsulot sonini tanlang", reply_markup=markup)


@dp.callback_query_handler(text_contains="number")
async def add_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    count = callback.data.split()[1]
    item_id = callback.data.split()[3]
    price = db.get_product(item_id)['price']
    title = db.get_product(item_id)['title']
    total = int(count) * price
    id =  (db.get_user(user_id)['id'])
    db.add_to_cart(id, item_id, count)
    await callback.message.answer(text = f"{count} dona {title} savatchaga qo'shildi", reply_markup = menu)


@dp.message_handler(text="Savatcha")
async def show_cart(message: types.Message):
    user = message.from_user
    markup = showcart()
    cart_items = db.get_cart(user.id)
    price = 0
    msg = ""
    # order_id = (db.get_order(message.from_user.id))['order_id']
    # print(order_id)
    
    for item in cart_items:
        product = db.get_product(item['product'])
        nom = db.get_subcategory(product['subcategory'])
        msg += f"<b>{nom['title']} {product['title']}</b>: {item['count']} ta, Narxi: {item['price']} so'm\n"
        price += int(item['price'])
    if price > 0:
        await message.answer(f"{msg}\n<b>Umumiy: {price}</b>", reply_markup=markup)
    else:
        await message.answer("Savatcha bo'sh", reply_markup=menu)


@dp.callback_query_handler(text_contains="clear")
async def clear_it(callback: CallbackQuery, **kwargs):
    db.clear_cart(callback.from_user.id)
    await callback.message.edit_text(text = "Savatcha tozalandi")


@dp.callback_query_handler(text_contains="buy")
async def buy_it(callback: CallbackQuery, **kwargs):
    user_id = callback.from_user.id
    markup = buy_item()
    await callback.message.edit_text(text = "To'lov turini tanlang", reply_markup=markup)


@dp.callback_query_handler(text_contains="cash")
async def get_contact(call: CallbackQuery, **kwargs):
    user_id = call.from_user.id
    await call.message.answer(text = "Manzilingizni jo'nating", reply_markup=location)


@dp.message_handler(content_types='location')
async def get_location(message: Message):
    locator = Nominatim(user_agent="myGeocoder")
    lat = message.location['latitude']
    lon = message.location['longitude']
    markup = confirm()
    locat = locator.reverse(f"{lat}, {lon}")
    await message.answer(text = f"Sizning manzilingiz: {locat.raw['display_name']}\nTasdiqlaysizmi?", reply_markup=markup)


@dp.callback_query_handler(text_contains="yes")
async def accept(call: CallbackQuery, **kwargs):
    await call.message.answer(text="Telefon raqamingizni jo'nating", reply_markup=contact)


@dp.callback_query_handler(text_contains="no")
async def ignore(call: CallbackQuery, **kwargs):
    await call.message.answer(text = "Manzilingizni aniqroq qilib jo'nating", reply_markup=location)


#Hammasi muvaffaqiyatli bo'lsa telefon nomerni so'rash
@dp.message_handler(content_types='contact')
async def success(message: Message):
    user_id = message.from_user.id
    cart_items = db.get_cart(message.from_user.id)
    number = message.contact['phone_number']
    client = message.contact['first_name']
    msg = ""
    price = 0
    if cart_items:
        for item in cart_items:
            product = db.get_product(item['product'])
            nom = db.get_subcategory(product['subcategory'])
            msg += f"<b>{nom['title']} {product['title']}</b>: {item['count']} ta, Narxi: {item['price']} so'm\n"
            price += int(item['price'])
        await bot.send_message(chat_id=ADMINS[0], text=f"Yangi buyurtma:\nRaqam: +{number}\nMijoz: {client}\n{msg}\n<b>Umumiy: {price}</b>")
        #ORDER CREATE YOZISH KERAK
        id =  (db.get_user(user_id)['user_id'])
        db.create_order(id, number, client, price)
        order_id = (db.get_order(message.from_user.id))['order_id']
        for item in cart_items:
            product = db.get_product(item['product'])
            db.create_orderproduct(order_id, product['id'], item['count'])
            print(product['id'])
        await message.answer(text = "Buyurtma qabul qilindi.\nTez orada sizga aloqaga chiqamiz😊", reply_markup = menu)
        db.clear_cart(user_id)
    else:
        await message.answer(text = "Avval biror mahsulot tanlab savatchaga qo'shing! 🛒", reply_markup=menu)


# Yuqoridagi barcha funksiyalar uchun yagona handler
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = int(callback_data.get("item_id"))

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories,  # Kategoriyalarni qaytaramiz
        "1": list_subcategories,  # Ost-kategoriyalarni qaytaramiz
        "2": list_items,  # Mahsulotlarni qaytaramiz
        "3": show_item,  # Mahsulotni ko'rsatamiz
        "4": send_count, # Mahsulot sonini tanlash uchun menu
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id
    )
