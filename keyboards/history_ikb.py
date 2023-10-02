from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_small_history_ikb() -> InlineKeyboardMarkup:
    """Метод возвращает инлпйн клавиатуру для исторического поискового запроса, если он только один"""
    my_ikb = InlineKeyboardMarkup()

    see_results_button = InlineKeyboardButton(text="Посмотреть результаты поиска", callback_data="show_results")
    my_ikb.add(see_results_button)

    return my_ikb


def get_history_ikb() -> InlineKeyboardMarkup:
    """Метод возвращает инлайн клавиатуру для поискового запроса с кнопками для просмотра след., пред. поиска или
    результатов поиска по данному запросу"""
    my_ikb = InlineKeyboardMarkup()

    previous_btn = InlineKeyboardButton(text="<<", callback_data="<<")
    see_results_button = InlineKeyboardButton(text="Билеты", callback_data="show_results")
    next_btn = InlineKeyboardButton(text=">>", callback_data=">>")

    my_ikb.add(previous_btn, see_results_button, next_btn)

    return my_ikb
