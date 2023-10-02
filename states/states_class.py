from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    """Класс состояний телеграм бота"""
    cheap_regim = State()
    cheap_from_city_wait = State()
    cheap_from_city_confirm = State()
    cheap_to_city_wait = State()
    cheap_to_city_confirm = State()
    cheap_return = State()
    cheap_start_period_month = State()
    cheap_start_period_date = State()
    cheap_period_choose = State()
    cheap_tickets_review = State()

    expensive_regim = State()
    expensive_from_city_wait = State()
    expensive_from_city_confirm = State()
    expensive_to_city_wait = State()
    expensive_to_city_confirm = State()
    expensive_return = State()
    expensive_start_period_month = State()
    expensive_start_period_date = State()
    expensive_period_choose = State()
    expensive_tickets_review = State()

    diapason_regim = State()
    diapason_from_city_wait = State()
    diapason_from_city_confirm = State()
    diapason_to_city_wait = State()
    diapason_to_city_confirm = State()
    diapason_return = State()
    diapason_start_period_month = State()
    diapason_start_period_date = State()
    diapason_period_choose = State()
    diapason_min_price_wait = State()
    diapason_max_price_wait = State()
    diapason_tickets_review = State()

    history = State()
