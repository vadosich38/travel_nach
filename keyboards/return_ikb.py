from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_return_ikb() -> InlineKeyboardMarkup:
    """Метод возвращает инлайн клавиатуру с выбором, нужны ли пользователю обратные билеты для перелета назад"""
    confirm_ikb = InlineKeyboardMarkup(row_width=1)
    without_return_btn = InlineKeyboardButton(text="Найти билеты в обе стороны", callback_data="false")
    with_return_btn = InlineKeyboardButton(text="Найти билеты только в одну сторону", callback_data="true")

    confirm_ikb.add(without_return_btn, with_return_btn)

    return confirm_ikb
