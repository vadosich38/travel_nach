from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def get_month_ikb(month: int = datetime.now().month) -> InlineKeyboardMarkup:
    """Функция создает и возвращает клавиатуру с 6ю месацами от выбранной даты"""
    month_dict = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
                  7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

    my_ikb = InlineKeyboardMarkup(row_width=2)

    for i in range(6):
        year = datetime.now().year
        month_numm = (month + i - 1) % 12 + 1

        formatted_month_num = f"0{month_numm}" if month_numm < 10 else str(month_numm)
        callback_data = f"{year + 1}-{formatted_month_num}" if month_numm < month else f"{year}-{formatted_month_num}"

        i_btn = InlineKeyboardButton(text=month_dict[month_numm], callback_data=callback_data)
        my_ikb.insert(i_btn)

    return my_ikb


def get_date_ikb(month: str) -> InlineKeyboardMarkup:
    """Функция возврашает клаивиатуру с датами месяца
    Месяца разбиты на 3 списка по продолжительности"""

    list_31days = ["01", "03", "05", "07", "08", "12"]
    list_30days = ["04", "06",  "09", "10", "11"]
    dates_ikb = InlineKeyboardMarkup(row_width=4)

    if datetime.now().month < 10 and f"0{datetime.now().month}" == month:
        date = datetime.now().day
    elif datetime.now().month > 10 and datetime.now().month == month:
        date = datetime.now().day
    else:
        date = 1

    if month in list_31days:
        for i_day in range(date, 32):
            day = f"0{date}" if date < 10 else str(date)

            date_btn = InlineKeyboardButton(text=str(date), callback_data=day)
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb

    elif month in list_30days:
        for i_day in range(date, 31):
            day = f"0{date}" if date < 10 else str(date)

            date_btn = InlineKeyboardButton(text=str(date), callback_data=day)
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb

    elif month == "02":
        for i_day in range(date, 29):
            day = f"0{date}" if date < 10 else str(date)

            date_btn = InlineKeyboardButton(text=str(date), callback_data=day)
            dates_ikb.insert(date_btn)
            date += 1
        return dates_ikb
