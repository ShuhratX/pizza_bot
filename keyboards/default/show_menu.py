from cgitb import text
import keyword
from urllib import request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню"),
            KeyboardButton(text="Корзина"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bosh menyu"),
            KeyboardButton(text="Savatcha"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


menu_cn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="主选单"),
            KeyboardButton(text="购物篮"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


contact_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard = [
        [
            KeyboardButton(text="Отправить контакт", request_contact=True)
        ],
        
    ]
    
)


contact_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard = [
        [
            KeyboardButton(text="Raqamni jo'natish", request_contact=True)
        ],
        
    ]
    
)



location_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📍 Отправить локацию",
                                request_location=True)
        ]
    ])


location_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📍 Manzilni jo'natish",
                                request_location=True)
        ]
    ])


# location_cn = ReplyKeyboardMarkup(
#     resize_keyboard=True,
#     one_time_keyboard=True,
#     keyboard=[
#         [
#             KeyboardButton(text="📍 Manzilni jo'natish",
#                                 request_location=True)
#         ]
#     ])