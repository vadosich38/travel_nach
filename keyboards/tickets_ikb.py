from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_tickets_ikb(link: str) -> InlineKeyboardMarkup:
    """Метод возвращает инлайн клавиатуру с кнопками для просмотра след., пред. билетов и кнопкой перехода на страницу
    покупки билетов"""
    my_ikb = InlineKeyboardMarkup(row_width=3)

    if link == "":
        link = "https://aviasales.com/"
    elif "." not in link:
        link = f"https://www.google.com/search?q={link}"

    previous_btn = InlineKeyboardButton(text="<<", callback_data="<<")
    link = InlineKeyboardButton(text="КУПИТЬ", url=link, callback_data="buy_ticket")
    next_btn = InlineKeyboardButton(text=">>", callback_data=">>")

    my_ikb.add(previous_btn, link, next_btn)

    return my_ikb


def get_small_tickets_ikb(link: str) -> InlineKeyboardMarkup:
    """Метод возвращает инлайн клавиатуру, если результат поиска содержит только один билет. Есть только кнопка для
    перехода на страницу покупки билета"""
    my_ikb = InlineKeyboardMarkup()

    if link == "":
        link = "https://aviasales.com/"
    elif "." not in link:
        link = f"https://www.google.com/search?q={link}"

    link = InlineKeyboardButton(text="КУПИТЬ", url=link, callback_data="buy_ticket")

    my_ikb.add(link)

    return my_ikb
