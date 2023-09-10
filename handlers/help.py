from set_tg_bot.dispatcher import my_disp
from aiogram import types
from texts.texts import HELP_TEXT
from keyboards.menu_kb import get_menu_kb


@my_disp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply(text=HELP_TEXT,
                        parse_mode="HTML",
                        reply_markup=get_menu_kb())
