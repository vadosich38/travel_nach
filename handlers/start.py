from set_tg_bot.dispatcher import my_disp
from aiogram import types
from texts.texts import START_TEXT
from keyboards.menu_kb import get_menu_kb


@my_disp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text=START_TEXT,
                         parse_mode="HTML",
                         reply_markup=get_menu_kb())
