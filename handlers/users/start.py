from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.show_menu import menu
from loader import dp, db, bot
from data.config import ADMINS

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # print(message.from_user.id)
    user = db.get_user(message.from_user.id)
    if user:
        await message.answer("Assalomu alaykum!\nQuyidagi Bosh menyu tugmasini bosing", reply_markup=menu,)
        
    else:
        db.add_user(
                telegram_id=message.from_user.id, 
                full_name=message.from_user.full_name,
                username=message.from_user.username,
            )
        await bot.send_message(chat_id=ADMINS[0], text=f"Yangi foydalanuvchi:\n{message.from_user.full_name}, {message.from_user.username}")
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nXush kelibsiz!\nMahsulotlarni ko'rish uchun quyidagi Bosh menyu tugmasini bosing",
        reply_markup=menu,)



@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_file_id_p(message: types.Message):
    await message.reply(message.photo[-1].file_id)