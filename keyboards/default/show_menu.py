from cgitb import text
import keyword
from urllib import request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bosh menyu"),
            KeyboardButton(text="Savatcha"),
        ],
    ],
    resize_keyboard=True,
)

contact = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard = [
        [
            KeyboardButton(text="Raqamni yuborish", request_contact=True)
        ],
        
    ]
    
)


location = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📍 Lokatsiya yuborish",
                                request_location=True)
        ]
    ])