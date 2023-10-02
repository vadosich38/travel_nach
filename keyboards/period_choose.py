from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_periods_ikb() -> InlineKeyboardMarkup:
    """Метод возвращает инлапйн клавиатуру со списоком периодов для выбора,
    в рамках которого будет произведен поиск билетов"""
    my_ikb = InlineKeyboardMarkup(row_width=2)

    day_btn = InlineKeyboardButton(text="Один день", callback_data="day")
    month_btn = InlineKeyboardButton(text="Один месяц", callback_data="month")
    season_btn = InlineKeyboardButton(text="Сезон", callback_data="season")
    year_btn = InlineKeyboardButton(text="Год", callback_data="year")

    my_ikb.add(day_btn)
    my_ikb.add(month_btn)
    my_ikb.add(season_btn)
    my_ikb.add(year_btn)

    return my_ikb
