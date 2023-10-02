from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirm_ikb() -> InlineKeyboardMarkup:
    """Метод возвращает инлайн клавиатуру с кнопкой подтверждения чего-либо"""
    confirm_ikb = InlineKeyboardMarkup(row_width=1)
    confirm_btn = InlineKeyboardButton(text="✅ Подтвердить ✅", callback_data="confirm")

    confirm_ikb.add(confirm_btn)

    return confirm_ikb
