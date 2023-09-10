from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_return_ikb() -> InlineKeyboardMarkup:
    confirm_ikb = InlineKeyboardMarkup(row_width=1)
    without_return_btn = InlineKeyboardButton(text="Только в одну сторону", callback_data="without_return")
    with_return_btn = InlineKeyboardButton(text="Туда и обратно", callback_data="with_return")

    confirm_ikb.add(without_return_btn, with_return_btn)

    return confirm_ikb
