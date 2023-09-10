from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    cheap_regim = State()
    cheap_from_city_wait = State()
    cheap_from_city_airport_choose = State()
    cheap_from_city_airport_confirm = State()
    cheap_to_city_wait = State()
    cheap_to_city_airport_choose = State()
    cheap_to_city_airport_confirm = State()
    cheap_return = State()
    cheap_to_month_wait = State()
    cheap_to_dates_wait = State()
    cheap_from_month_wait = State()
    cheap_from_dates_wait = State()
    cheap_return_month_wait = State()
    cheap_return_dates_wait = State()

    expensive_regim = State()
    expensive_from_city_wait = State()
    expensive_to_city_wait = State()
    expensive_dates_wait = State()

    range_regim = State()
    range_min = State()
    range_max = State()
    range_from_city_wait = State()
    range_to_city_wait = State()
    range_dates_wait = State()
