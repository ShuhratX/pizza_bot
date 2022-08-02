from sre_constants import IN
from turtle import title
from typing import Union
from keyboards.default.show_menu import contact_ru, contact_uz, location_ru, location_uz, menu_ru, menu_uz
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
    confirm,
    pay
)
from loader import dp, db, bot

lang = ''

@dp.callback_query_handler(text_contains="RUS")
async def lang_ru(callback: CallbackQuery, **kwargs):
    global lang
    lang = 'ru'
    await callback.message.edit_text(text="Язык выбран")
    await callback.message.answer(text="Пожалуйста, выберите товар", reply_markup=menu_ru)


@dp.callback_query_handler(text_contains="UZB")
async def lang_uz(callback: CallbackQuery, **kwargs):
    global lang
    lang = 'uz'
    
    await callback.message.edit_text(text="Til tanlandi")
    await callback.message.answer(text="Iltimos maxsulot tanlang", reply_markup=menu_uz)


# @dp.callback_query_handler(text_contains="CHINA")
# async def lang_uz(callback: CallbackQuery, **kwargs):
#     global lang
#     lang = 'uz'
    
#     await callback.message.edit_text(text="Til tanlandi")
#     await callback.message.answer(text="Iltimos maxsulot tanlang", reply_markup=menu_uz)


# Bosh menyu matni uchun handler
@dp.message_handler(text="Главное меню")
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    global lang
    lang = 'ru'
    await list_categories(message)


@dp.message_handler(text="Bosh menyu")
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    global lang
    lang = 'uz'
    await list_categories(message)


@dp.message_handler(text="主选单")
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    global lang
    lang = '🇨🇳'
    await list_categories(message)

# Kategoriyalarni qaytaruvchi funksiya. Callback query yoki Message qabul qilishi ham mumkin.
# **kwargs yordamida esa boshqa parametrlarni ham qabul qiladi: (category, subcategory, item_id)
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Keyboardni chaqiramiz
    markup = await categories_keyboard(lang=lang)
    # print(lang)
    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        if lang == 'ru':
            await message.answer("<b>Выберите категорию</b>", reply_markup=markup)
        elif lang == 'uz':
            await message.answer("<b>Kategoriya tanlang</b>", reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Ost-kategoriyalarni qaytaruvchi funksiya
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(lang, category)

    # Xabar matnini o'zgartiramiz va keyboardni yuboramiz
    await callback.message.edit_reply_markup(markup)


# Ost-kategoriyaga tegishli mahsulotlar ro'yxatini yuboruvchi funksiya
async def list_items(callback: CallbackQuery, subcategory, one, two, **kwargs):
    markup = await items_keyboard(lang, subcategory, one, two)
    text = ''
    if lang == 'ru':
        text = "<b>Выберите продукт</b>"
    elif lang == 'uz':
        text = "<b>Maxsulot tanlang</b>"
    await callback.message.edit_text(text=text, reply_markup=markup)


# Biror mahsulot uchun Xarid qilish tugmasini yuboruvchi funksiya
async def show_item(callback: CallbackQuery, item_id, one, two, **kwargs):
    markup = item_keyboard(lang, item_id, one, two)

    # Mahsulot haqida ma'lumotni bazadan olamiz
    item = db.get_product(item_id)

    if lang == 'ru':
        title = item['title']
        price = 'Цена'
        prc = 'сум'
    elif lang == 'uz':
        title = item['title_uz']
        price = 'Narxi'
        prc = "so'm"

    if item['image']:
        text = f"<a href=\"{item['image']}\">{title}</a>\n\n"
    else:
        text = f"{title}\n\n"
    text += f"{price}: {item['price']} {prc}"

    await callback.message.edit_text(text=text, reply_markup=markup)


async def send_count(callback: CallbackQuery, item_id, **kwargs):
    markup = count_keyboard(lang, item_id)
    item = db.get_product(item_id)
    text = ''
    if lang == 'ru':
        if item['image']:
            text = f"<a href=\"{item['image']}\">{item['title']}</a>\n\nВыберите количество продуктов:\n "
        else:
            text = f"{item['title']}\n\nВыберите количество продуктов:\n "
    elif lang == 'uz':
        if item['image']:
            text = f"<a href=\"{item['image']}\">{item['title_uz']}</a>\n\nMaxsulot sonini tanlang:\n "
        else:
            text = f"{item['title']}\n\nMaxsulot sonini tanlang:\n "
    
    await callback.message.edit_text(text = text, reply_markup=markup)


@dp.callback_query_handler(text_contains="number")
async def add_cart(callback: CallbackQuery):
    markup = InlineKeyboardMarkup()
    user_id = callback.from_user.id
    count = callback.data.split()[1]
    item_id = callback.data.split()[3]
    price = db.get_product(item_id)['price']
    title_ru = db.get_product(item_id)['title']
    title_uz = db.get_product(item_id)['title_uz']
    total = int(count) * price
    id =  (db.get_user(user_id)['user_id'])
    db.add_to_cart(id, item_id, count)
    text = ''
    text2 = ''
    menu = ''
    if lang == 'ru':
        text = f"Продукт <b>{title_ru}</b> успешно добавлен в корзину ✅"
        text2 = "Продолжим?"
        menu = menu_ru
    elif lang == 'uz':
        text = f"<b>{title_uz}</b> maxsuloti savatchaga qo'shildi ✅"
        text2 = "Davom ettirasizmi?"
        menu = menu_uz
    await callback.message.edit_text(text = text, reply_markup = markup)
    await callback.message.answer(text = text2, reply_markup = menu)


@dp.message_handler(text="Savatcha")
async def show_cart(message: types.Message):
    user = message.from_user
    markup = showcart(lang)
    cart_items = db.get_cart(user.id)
    price = 0
    msg = ""
    
    for item in cart_items:
        product = db.get_product(item['product'])
        # nom = db.get_subcategory(product['subcategory'])
        msg += f"<b>{product['title_uz']}</b>\nSoni {item['count']}, Narxi: {item['price']} so'm\n"
        price += int(item['price'])
    if price > 0:
        await message.answer(f"{msg}\n<b>Jami: {price}</b> so'm", reply_markup=markup)
    else:
        await message.answer("Savatcha bo'sh", reply_markup=menu_uz)


@dp.message_handler(text="Корзина")
async def show_cart(message: types.Message):
    user = message.from_user
    markup = showcart(lang)
    cart_items = db.get_cart(user.id)
    price = 0
    msg = ""
    
    for item in cart_items:
        product = db.get_product(item['product'])
        # nom = db.get_subcategory(product['subcategory'])
        msg += f"<b>{product['title']}</b>\nКоличество {item['count']}, Цена: {item['price']} сум\n"
        price += int(item['price'])
    if price > 0:
        await message.answer(f"{msg}\n<b>Итого: {price}</b> сум", reply_markup=markup)
    else:
        await message.answer("Корзина пуста", reply_markup=menu_ru)


@dp.callback_query_handler(text_contains="clear")
async def clear_it(callback: CallbackQuery, **kwargs):
    db.clear_cart(callback.from_user.id)
    text = ''
    if lang == 'ru':
        text = "Корзина очищена"
    elif lang == 'uz':
        text = "Savatcha tozalandi"
    await callback.message.edit_text(text = text)


# @dp.callback_query_handler(text_contains="buy")  

# async def buy_it(callback: CallbackQuery, **kwargs):
#     user_id = callback.from_user.id
#     markup = buy_item(lang)
#     text = ''
#     if lang == 'ru':
#         text = "<b>Выберите способ оплаты:</b>"
#     elif lang == 'uz':
#         text = "<b>To'lov turini tanlang</b>"
#     await callback.message.edit_text(text = text, reply_markup=markup)


@dp.callback_query_handler(text_contains="buy")
async def get_location(callback: CallbackQuery, **kwargs):
    markup = InlineKeyboardMarkup()

    loc = ''
    locat = ''
    if lang == 'ru':
        adrs = "Адрес доставки"
        loc = 'Отправьте свою геолокацию'
        locat =  location_ru
    elif lang == 'uz':
        adrs = "Yetkazib berish manzili"
        loc = "Manzilingizni jo'nating"
        locat =  location_uz
    elif lang == 'cn':
        adrs = "送货地点"
        loc = "请发送您的定位"
        locat =  location_uz
    await callback.message.edit_text(text = adrs, reply_markup=markup)
    await callback.message.answer(text = loc, reply_markup=locat)


location_client = ""

@dp.message_handler(content_types='location')
async def get_location(message: Message):
    locator = Nominatim(user_agent="myGeocoder")
    lat = message.location['latitude']
    lon = message.location['longitude']
    global location_client
    text = ''
    text2 = ''
    if lang == 'ru':
        text = "Ваш адрес:"
        text2 = 'Вы подтверждаете?'
    elif lang == 'uz':
        text = "Sizning manzil:"
        text2 = "Tasdiqlaysizmi?"
    location_client = message.location
    markup = confirm(lang)
    locat = locator.reverse(f"{lat}, {lon}")
    await message.answer(text = f"{text} {locat.raw['display_name']}\n{text2}", reply_markup=markup)


@dp.callback_query_handler(text_contains="yes")  
async def accept(callback: CallbackQuery, **kwargs):
    text = ''
    text2 = ''
    contact = ''
    rem = InlineKeyboardMarkup()
    if lang == 'ru':
        text = 'Подтверждено'
        text2 = "Пожалуйста, отправьте свой номер телефона"
        contact = contact_ru
    elif lang == 'uz':
        text = 'Tasdiqlandi'
        text2 = "Telefon raqamingizni jo'nating"
        contact = contact_uz
    elif lang == 'cn':
        text = '确认'
        text2 = "请确认您的电话号码"
        contact = contact_uz
    await callback.message.edit_text(text = text, reply_markup=rem)
    await callback.message.answer(text=text2, reply_markup=contact)


@dp.callback_query_handler(text_contains="no")
async def ignore(call: CallbackQuery, **kwargs):
    text = ''
    location = ''
    if lang == 'ru':
        text = "Отправьте свой адрес более точно"
        location = location_ru
    elif lang == 'uz':
        text = "Manzilingizni aniqroq qilib jo'nating"
        location = location_uz
    await call.message.answer(text = text, reply_markup=location)

number = ''
cliyent = ''
#Hammasi muvaffaqiyatli bo'lsa telefon nomerni so'rash
@dp.message_handler(content_types='contact')
async def payment(message: Message):
    user_id = message.from_user.id
    global number
    global cliyent
    number = message.contact['phone_number']
    cliyent = message.contact['first_name']
    markup = buy_item(lang)
    text = ''
    text2 = ''
    if lang == 'ru':
        text = "<b>Контакт получен</b>"
        text2 = "<b>Выберите способ оплаты:</b>"
    elif lang == 'uz':
        text = "<b>Kontakt qabul qilindi</b>"
        text2 = "<b>To'lov turini tanlang</b>"
    elif lang == 'cn':
        text = "<b>验收人电话号码</b>"
        text2 = "<b>选择付款方式，谢谢合作</b>"
        
    await message.answer(text = text, reply_markup=ReplyKeyboardRemove())
    await message.answer(text = text2, reply_markup=markup)


@dp.callback_query_handler(text_contains="cash")
async def success(callback: CallbackQuery, **kwargs):
    cart_items = db.get_cart(callback.from_user.id)
    user_id = callback.from_user.id
    buying_type = ''
    if lang == 'ru':
        buying_type = "Оплата по карте"
    elif lang == 'uz':
        buying_type = "Karta orqali to'lov"
    msg = ""
    price = 0
    text1 = ''
    text2 = ''
    text3 = ''
    text4 = ''
    menu = ''
    if lang == 'ru':
        text1 = "Новый заказ:\nНомер телефона"
        text2 = "Ваш заказ принят.\nМы свяжемся с вами в ближайшее время😊"
        text3 = "Сначала выберите продукт и продолжайте заказ! 🛒"
        text4 = ["Покупатель", "Итого", "сум", "Cпособ оплаты", "Адрес"]
        menu = menu_ru
    if lang == 'uz':
        text1 = "Yangi buyurtma:\nTelefon raqami"
        text2 = "Buyurtmangiz qabul qilindi.\nTez orada siz bilan bog'lanamiz😊"
        text3 = "Avval biror maxsulotni tanlab savatchaga qo'shing! 🛒"
        text4 = ["Mijoz", "Jami", "so'm", "To'lov turi", "Manzil"]
        menu = menu_uz
    if lang == 'cn':
        text1 = "Yangi buyurtma:\Telefon raqami"
        text2 = "订单成功，服务员稍后和您联系。谢谢您的支持🙏"
        text3 = "Avval biror maxsulotni tanlab savatchaga qo'shing! 🛒"
        text4 = ["Mijoz", "Jami", "so'm", "To'lov turi", "Manzil"]
        menu = menu_uz    
    if cart_items:
        for item in cart_items:
            product = db.get_product(item['product'])
            nom = db.get_subcategory(product['subcategory'])
            if lang == 'ru':
                msg += f"<b>{nom['title']} > {product['title']}</b>: {item['count']} ta,\nЦена: {item['price']} сум\n"
            elif lang == 'uz':
                msg += f"<b>{nom['title_uz']} > {product['title_uz']}</b>: {item['count']} ta,\nNarxi: {item['price']} so'm\n"
            price += int(item['price'])
        await bot.send_message(chat_id=ADMINS[0], text=f"{text1}: {number}\n{text4[0]}: {cliyent}\n{msg}\n<b>{text4[1]}: {price}</b> {text4[2]}\n{text4[3]}: {buying_type}\n\n{text4[4]}: https://maps.google.com/maps?q={location_client['latitude']},{location_client['longitude']}&ll={location_client['latitude']},{location_client['longitude']}&z=16")
        #ORDER CREATE YOZISH KERAK
        id = (db.get_user(user_id)['user_id'])
        db.create_order(id, number, cliyent, price)
        order_id = (db.get_order(user_id))['order_id']
        for item in cart_items:
            product = db.get_product(item['product'])
            db.create_orderproduct(order_id, product['id'], item['count'])
            # print(product['id'])
        await callback.message.answer(text = text2, protect_content=True, reply_markup = menu)
        db.clear_cart(user_id)
    else:
        await callback.message.answer(text = text3, reply_markup=menu)


@dp.callback_query_handler(text_contains="by_cart")
async def success(callback: CallbackQuery, **kwargs):
    markup = InlineKeyboardMarkup()
    buying_type = ''
    user_id = callback.from_user.id
    if lang == 'ru':
        buying_type = "Оплата по карте"
    elif lang == 'uz':
        buying_type = "Karta orqali to'lov"
    
    cart_items = db.get_cart(user_id)
    pay_it = pay(lang)
    msg = ""
    price = 0
    text1 = ''
    text2 = ''
    text3 = ''
    text4 = ''
    menu = ''
    if lang == 'ru':
        text1 = "Новый заказ:\nНомер телефона"
        text2 = "Ваш заказ принят.\nНажмите на кнопку ниже, чтобы оплатить😊"
        text3 = "Сначала выберите продукт и продолжайте заказ! 🛒"
        text4 = ["Покупатель", "Итого", "сум", "Cпособ оплаты", "Адрес"]
        menu = menu_ru
    if lang == 'uz':
        text1 = "Yangi buyurtma:\nTelefon raqami"
        text2 = "Buyurtmangiz qabul qilindi.\nTo'lov uchun quyidagi tugmani bosing😊"
        text3 = "Avval biror maxsulotni tanlab savatchaga qo'shing! 🛒"
        text4 = ["Mijoz", "Jami", "so'm", "To'lov turi", "Manzil"]
        menu = menu_uz
    if cart_items:
        for item in cart_items:
            product = db.get_product(item['product'])
            nom = db.get_subcategory(product['subcategory'])
            if lang == 'ru':
                msg += f"<b>{nom['title']} > {product['title']}</b>: {item['count']} ta,\nЦена: {item['price']} сум\n"
            elif lang == 'uz':
                msg += f"<b>{nom['title_uz']} > {product['title_uz']}</b>: {item['count']} ta,\nNarxi: {item['price']} so'm\n"
            price += int(item['price'])
        await bot.send_message(chat_id=ADMINS[0], text=f"{text1}: {number}\n{text4[0]}: {cliyent}\n{msg}\n<b>{text4[1]}: {price}</b> {text4[2]}\n{text4[3]}: {buying_type}\n\n{text4[4]}: https://maps.google.com/maps?q={location_client['latitude']},{location_client['longitude']}&ll={location_client['latitude']},{location_client['longitude']}&z=16")
        #ORDER CREATE YOZISH KERAK
        id = (db.get_user(user_id)['user_id'])
        db.create_order(id, number, cliyent, price)
        order_id = (db.get_order(user_id))['order_id']
        for item in cart_items:
            product = db.get_product(item['product'])
            db.create_orderproduct(order_id, product['id'], item['count'])
            # print(product['id'])
        await callback.message.edit_text(text = text2, reply_markup=pay_it)
        # await callback.message.answer(text = text2, reply_markup = pay_it)
        db.clear_cart(user_id)
    else:
        await callback.message.edit_text(text = buying_type, reply_markup=markup)
        await callback.message.answer(text = text3, reply_markup=menu)


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

    one = int(callback_data.get("one"))

    two = int(callback_data.get("two"))

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
        call, category=category, subcategory=subcategory, item_id=item_id, one=one, two=two
    )