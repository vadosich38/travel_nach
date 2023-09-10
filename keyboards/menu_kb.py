from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_kb() -> ReplyKeyboardMarkup:
    my_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=False,
                                row_width=2)

    btn_low = KeyboardButton(text="💸 Найти дешевые билеты 💸")
    btn_high = KeyboardButton(text="✈️ Найти дорогие билеты ✈️")
    btn_range = KeyboardButton(text="🛩 Найти билеты в дипазоне цен 🛩")
    btn_history = KeyboardButton(text="🚀 Посмотреть историю запросов 🚀")

    my_kb.add(btn_low, btn_high, btn_range, btn_history)

    return my_kb
