from set_tg_bot.dispatcher import my_disp
from set_tg_bot.bot import my_bot
from aiogram import types
from states.states_class import BotStates
from db_methods.db_class import DBMethods
from db_methods.connections import history_db_connect
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards.cancel_kb import get_cancel_kb
from keyboards.menu_kb import get_menu_kb
from keyboards.history_ikb import get_small_history_ikb, get_history_ikb
from texts.texts import get_history_text, get_listing_text
from api_package.api_class import ApiMethods
from processing.city_checker import check_city
from keyboards.tickets_ikb import get_tickets_ikb, get_small_tickets_ikb


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.history)
async def cmd_cancel_from_city_wait(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text, Text(equals="🚀 Посмотреть историю запросов 🚀",
                                                            ignore_case=False))
async def get_history(message: types.Message, state: FSMContext):
    """Функция хендлер принимает команду ИСТОРИЯ ЗАПРОСОВ
    Возвращает сообщение где указаны параметры поиска с клавиатурой, где есть три кнопки:
    Предыдущий поиск
    Следущий поиск
    Показать результаты поиска"""

    await message.reply(text="📸 Ищем историю ваших запросов 📸", reply_markup=get_cancel_kb())

    async with state.proxy() as data:
        data["curr_history_search"] = 0
        data["user_history"] = DBMethods.get_user_searches(user_id=message.from_user.id, conn=history_db_connect)
        data["history_searches_count"] = len(data["user_history"])

    text = get_history_text(data=data)

    if data["history_searches_count"] > 1:
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text=text,
                                  parse_mode="HTML",
                                  reply_markup=get_history_ikb())
        await BotStates.history.set()
    elif data["history_searches_count"] == 1:
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text=text,
                                  parse_mode="HTML",
                                  reply_markup=get_small_history_ikb())
        await state.finish()
    else:
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text="У вас нет истории запросов 😢",
                                  reply_markup=get_menu_kb())
        await state.finish()


@my_disp.callback_query_handler(state=BotStates.history, text=">>")
async def next_search(callback_data: types.CallbackQuery, state: FSMContext):
    """Фукнция колбек хендлер возвращает следующий исторический поисковый запрос пользователя"""
    await callback_data.answer(text="Следующий исторический запрос")

    async with state.proxy() as data:
        if data["curr_history_search"] + 1 == data["history_searches_count"]:
            data["curr_history_search"] = 0
        else:
            data["curr_history_search"] += 1

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   parse_mode="HTML",
                                   text=get_history_text(data=data),
                                   reply_markup=get_history_ikb())


@my_disp.callback_query_handler(state=BotStates.history, text="<<")
async def previous_search(callback_data: types.CallbackQuery, state: FSMContext):
    """Фукнция колбек хендлер возвращает предыдущий исторический поисковый запрос пользователя"""
    await callback_data.answer(text="Предыдущий исторический запрос")

    async with state.proxy() as data:
        if data["curr_history_search"] == 0:
            data["curr_history_search"] = data["history_searches_count"] - 1
        else:
            data["curr_history_search"] -= 1

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text=get_history_text(data=data),
                                   parse_mode="HTML",
                                   reply_markup=get_history_ikb())


@my_disp.callback_query_handler(state=BotStates.history, text="show_results")
async def research_history_search(callback_data: types.CallbackQuery, state: FSMContext):
    """Фукнция колбек хендлер возвращает новые результаты поиска по историчкскому поисковому запросу
    При этом данный запрос не записывается в БД снова"""
    await callback_data.answer(text="Ищу билеты по вашему запросу...")
    async with state.proxy() as data:
        from_city = check_city(city_name=data['user_history'][data['curr_history_search']][3])
        to_city = check_city(city_name=data['user_history'][data['curr_history_search']][4])

        data["curr_ticket"] = 0
        data["from_iata"] = DBMethods.get_city_iata(city_name=from_city[0], language=from_city[1])
        data["to_iata"] = DBMethods.get_city_iata(city_name=to_city[0], language=from_city[1])
        data["start_date"] = data['user_history'][data['curr_history_search']][5]
        data["period"] = data['user_history'][data['curr_history_search']][6]
        data["return"] = data['user_history'][data['curr_history_search']][7].capitalize()
        data["search_type"] = data['user_history'][data['curr_history_search']][2]
        data["min_price"] = data['user_history'][data['curr_history_search']][8]
        data["max_price"] = data['user_history'][data['curr_history_search']][9]

    if data["search_type"] == "Самые дешевые билеты":
        tickets_bundle = ApiMethods.get_cheapest_tickets(from_city=data["from_iata"],
                                                         to_city=data["to_iata"],
                                                         date=data["start_date"],
                                                         period=data["period"],
                                                         one_way=data["return"])
        async with state.proxy() as data:
            data["tickets_bundle"] = tickets_bundle
            data["tickets_count"] = len(tickets_bundle)

        if data["tickets_count"] > 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data, tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.cheap_tickets_review.set()
        elif data["tickets_count"] == 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data, tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_small_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.cheap_tickets_review.set()

        else:
            await callback_data.message.delete()
            await my_bot.send_message(chat_id=callback_data.from_user.id,
                                      text="Билеты не найдены. Попробуйте найти самостоятельно на aviasales.com",
                                      reply_markup=get_menu_kb())
            await state.finish()

    elif data["search_type"] == "Диапазон цен":
        tickets_bundle = ApiMethods.get_diapason_tickets(from_city=data["from_iata"],
                                                         to_city=data["to_iata"],
                                                         date=data["start_date"],
                                                         period=data["period"],
                                                         one_way=data["return"],
                                                         min_price=data["min_price"],
                                                         max_price=data["max_price"])
        async with state.proxy() as data:
            data["tickets_bundle"] = tickets_bundle
            data["tickets_count"] = len(tickets_bundle)

        if data["tickets_count"] > 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data,
                                                                 tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.diapason_tickets_review.set()
        elif data["tickets_count"] == 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data,
                                                                 tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_small_tickets_ikb(
                                               link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.diapason_tickets_review.set()
        else:
            await callback_data.message.delete()
            await my_bot.send_message(chat_id=callback_data.from_user.id,
                                      text="Билеты не найдены. Попробуйте найти самостоятельно на aviasales.com",
                                      reply_markup=get_menu_kb())

    elif data["search_type"] == "Самые дорогие билеты":
        tickets_bundle = ApiMethods.get_expensive_tickets(from_city=data["from_iata"],
                                                          to_city=data["to_iata"],
                                                          date=data["start_date"],
                                                          period=data["period"],
                                                          one_way=data["return"])
        async with state.proxy() as data:
            data["tickets_bundle"] = tickets_bundle
            data["tickets_count"] = len(tickets_bundle)

        if data["tickets_count"] > 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data,
                                                                 tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.expensive_tickets_review.set()
        elif data["tickets_count"] == 1:
            await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                           message_id=callback_data.message.message_id,
                                           text=get_listing_text(data=data,
                                                                 tickets_bundle=tickets_bundle),
                                           parse_mode="HTML",
                                           reply_markup=get_small_tickets_ikb(
                                               link=tickets_bundle[data["curr_ticket"]]['gate']))

            await BotStates.expensive_tickets_review.set()
        else:
            await callback_data.message.delete()
            await my_bot.send_message(chat_id=callback_data.from_user.id,
                                      text="Билеты не найдены. Попробуйте найти самостоятельно на aviasales.com",
                                      reply_markup=get_menu_kb())


