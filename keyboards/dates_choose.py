from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def get_month_ikb(month: int = datetime.now().month) -> InlineKeyboardMarkup:
    months_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    my_ikb = InlineKeyboardMarkup(row_width=2)
    for i in range(6):
        index = (month + i - 1) % 12
        if index+1 < month:
            i_btn = InlineKeyboardButton(text=months_list[index], callback_data=f"{datetime.now().year+1}-{index}")
        else:
            i_btn = InlineKeyboardButton(text=months_list[index], callback_data=f"{datetime.now().year}-{index}")

        my_ikb.add(i_btn)

    return my_ikb


def get_date_ikb(month: str, date: int = 1, same_month: bool = False) -> InlineKeyboardMarkup:
    list_31days = ["0", "2", "4", "6", "7", "11"]
    list_30days = ["3", "5",  "8", "9", "10"]
    dates_ikb = InlineKeyboardMarkup(row_width=4)

    if datetime.now().month - 1 == int(month):
        date = datetime.now().day
        same_month = True
    if not same_month:
        date = 1

    if month in list_31days:
        for i_day in range(date, 32):
            date_btn = InlineKeyboardButton(text=str(date), callback_data=str(date))
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb
    elif month in list_30days:
        for i_day in range(date, 31):
            date_btn = InlineKeyboardButton(text=str(date), callback_data=str(date))
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb
    elif month == "1":
        for i_day in range(date, 29):
            date_btn = InlineKeyboardButton(text=str(date), callback_data=str(date))
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb
