from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.show_menu import menu_ru
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.inline.menu_keyboards import change_lang
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # print(message.from_user.id)
    user = db.get_user(message.from_user.id)

    if user:
        await message.answer("Здравствуйте! Добро пожаловать в службу доставки ресторана \"<b>China Xibei</b>\"\nВыберите язык", reply_markup=change_lang(),)
        
    else:
        db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
            )

        await bot.send_message(chat_id=ADMINS[0], text=f"Новый пользователь:{message.from_user.full_name}\nUsername: {message.from_user.username}")
        await message.answer(f"Здравствуйте!, {message.from_user.full_name}!\nДобро пожаловать в службу доставки ресторана \"<b>China Xibei</b>\"\nВыберите язык", reply_markup=change_lang())



@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_file_id_p(message: types.Message):
    await message.reply(message.photo[-1].file_id)