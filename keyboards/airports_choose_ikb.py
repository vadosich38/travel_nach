from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_airports_ikb(airports: tuple) -> InlineKeyboardMarkup:
    airports_ikb = InlineKeyboardMarkup(row_width=2)

    for i_airport in airports:
        airport_btn = InlineKeyboardButton(text=i_airport[0],
                                           callback_data=i_airport[0])
        airports_ikb.add(airport_btn)
    no_matter_btn = InlineKeyboardButton(text="Не имеет значения",
                                         callback_data="!")
    airports_ikb.add(no_matter_btn)

    return airports_ikb
