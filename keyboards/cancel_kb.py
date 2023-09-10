from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cancel_kb() -> ReplyKeyboardMarkup:
    my_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True)
    cancel_btn = KeyboardButton(text="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥")
    my_kb.add(cancel_btn)
    return my_kb
