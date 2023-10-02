from datetime import datetime


START_TEXT = """<b>Добро пожаловать в Travel Bot</b>
<i>В этом боте вы сможете найти некоторую информацию о перелетах</i>

<b>Воспользуйтесь командой /help для просмотра возможностей бота</b>"""

HELP_TEXT = """
<b>Список команд бота</b>

<b>/low</b><i> –– найти самые дешевые перелеты</i>
<b>/high</b><i> –– найти самые дорогие перелеты</i>
<b>/custom</b><i> –– найти перелеты в вашем диапазоне цен</i>
<b>/history</b><i> –– показать историю запросов</i>"""


def get_listing_text(data: dict, tickets_bundle: list) -> str:
    """Метод создает и возвращает текст для сообщения, где представляется предложение перелета и описаны его свойства"""
    if tickets_bundle[data['curr_ticket']]['trip_class'] == 0:
        trip_class = "Эконом"
    elif tickets_bundle[data['curr_ticket']]['trip_class'] == 1:
        trip_class = "Бизнес"
    else:
        trip_class = "Первый"

    if data["return"] == "False" or data["return"] == "false":
        depart_date = datetime.strptime(tickets_bundle[data['curr_ticket']]['depart_date'][:10], "%Y-%m-%d")
        return_date = datetime.strptime(tickets_bundle[data['curr_ticket']]['return_date'][:10], "%Y-%m-%d")
        days = (return_date - depart_date).days

        text = f"✳️ <b>ПРЕДЛОЖЕНИЕ {data['tickets_count'] - (data['tickets_count'] - 1 - data['curr_ticket'])}</b>\n\n"\
               f"💰 Цена билетов: {tickets_bundle[data['curr_ticket']]['value']} €\n" \
               f"⏰ Дата вылета: {tickets_bundle[data['curr_ticket']]['depart_date'][:10]}" \
               f" в {tickets_bundle[data['curr_ticket']]['depart_date'][11:16]}\n" \
               f"⏰ Дата обратного вылета: {tickets_bundle[data['curr_ticket']]['return_date'][:10]}" \
               f" в {tickets_bundle[data['curr_ticket']]['return_date'][11:16]}\n" \
               f"⏳ Дней в городе назначения: {days}\n" \
               f"🫡 Класс: {trip_class}"
    else:
        text = f"✳️ ПРЕДЛОЖЕНИЕ {data['tickets_count'] - (data['tickets_count'] - 1 - data['curr_ticket'])}\n\n" \
               f"💰 Цена билета: {tickets_bundle[data['curr_ticket']]['value']} €\n" \
               f"⏰ Дата вылета: {tickets_bundle[data['curr_ticket']]['depart_date'][:10]}" \
               f" в {tickets_bundle[data['curr_ticket']]['depart_date'][11:16]}\n" \
               f"🫡 Класс: {trip_class}"\

    return text


def get_history_text(data: dict) -> str:
    """Метод формирует и возвращает текст для описания и представления исторического пользовательского запроса"""
    if bool(data['user_history'][data['curr_history_search']][7].capitalize()):
        text = f"<b>Поиск №{data['curr_history_search'] + 1}</b>\n\n"\
               f"🛫 Вы летели из: {data['user_history'][data['curr_history_search']][3]}\n"\
               f"🛩 Вы летели в: {data['user_history'][data['curr_history_search']][4]}\n"\
               f"📅 Дата начала поиска билетов: {data['user_history'][data['curr_history_search']][5]}\n"\
               f"📈 Период поиска билетов: {data['user_history'][data['curr_history_search']][6]}\n" \
               f"📍 Обратный рейс включен в цену\n"\
               f"🔍 Тип поискового запроса: {data['user_history'][data['curr_history_search']][2]}\n"

    else:
        text = f"<b>Поиск №{[data['curr_history_search'] + 1]}</b>\n\n"\
               f"🛫 Вы летели из: {data['user_history'][data['curr_history_search']][3]}\n"\
               f"🛩 Вы летели в: {data['user_history'][data['curr_history_search']][4]}\n"\
               f"📅 Дата начала поиска билетов: {data['user_history'][data['curr_history_search']][5]}\n"\
               f"📈 Период поиска билетов: {data['user_history'][data['curr_history_search']][6]}\n" \
               f"📍 Обратный рейс НЕ включен в цену\n"\
               f"🔍 Тип поискового запроса: {data['user_history'][data['curr_history_search']][2]}\n"

    return text

