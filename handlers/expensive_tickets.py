from set_tg_bot.dispatcher import my_disp
from set_tg_bot.bot import my_bot
from states.states_class import BotStates
from processing.city_checker import check_city
from db_methods.db_class import DBMethods
from keyboards.cancel_kb import get_cancel_kb
from keyboards.menu_kb import get_menu_kb
from keyboards.confirm_ikb import get_confirm_ikb
from keyboards.return_ikb import get_return_ikb
from api_package.api_class import ApiMethods
from keyboards.dates_choose import get_month_ikb, get_date_ikb
from keyboards.period_choose import get_periods_ikb
from db_methods.connections import history_db_connect
from keyboards.tickets_ikb import get_small_tickets_ikb, get_tickets_ikb
from texts.texts import get_listing_text

from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext


@my_disp.message_handler(lambda message: message.text, Text(equals="✈️ Найти дорогие билеты ✈️", ignore_case=False))
async def cmd_expensive_regim(message: types.Message):
    await message.reply(text="<b>Давайте найдем самые дорогие билеты для вашего перелета 👀</b>\n\n"
                             "Из какого города вы летите? ✈️",
                        parse_mode='HTML',
                        reply_markup=get_cancel_kb())
    await BotStates.expensive_from_city_wait.set()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_from_city_wait)
async def cmd_cancel_from_city_wait(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_from_city_confirm)
async def cmd_cancel_from_city_confirm(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_to_city_wait)
async def cmd_cancel_to_city_wait(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_to_city_confirm)
async def cmd_cancel_to_city_confirm(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_return)
async def cmd_cancel_return(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_start_period_month)
async def cmd_cancel_start_period_month(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_start_period_date)
async def cmd_cancel_start_period_date(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_period_choose)
async def cmd_cancel_period_choose(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.expensive_tickets_review)
async def cmd_cancel_tickets_review(message: types.Message, state: FSMContext):
    """Функция хендлер обрабатывает кнопку возврата в главное меню"""
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text, state=BotStates.expensive_from_city_wait)
async def from_city(message: types.Message, state: FSMContext):
    """Функция хендлер получает и записывает город вылета"""
    check_res = check_city(city_name=message.text)

    async with state.proxy() as data:
        data["from_city"] = check_res[0]
        from_city_iata = DBMethods.get_city_iata(city_name=check_res[0], language=check_res[1])
        if from_city_iata:
            data["from_city_iata"] = from_city_iata[0]
            await my_bot.send_message(chat_id=message.from_user.id,
                                      text=f"\n🛫 Вы вылетаете из города <b>{data['from_city']}</b> 🛫"
                                           f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР ГОРОДА ВЫЛЕТА</b>",
                                      parse_mode="HTML",
                                      reply_markup=get_confirm_ikb())
            await BotStates.expensive_from_city_confirm.set()

        else:
            await message.reply(text="Вы ввели город не корректно либо в нем нет аэропортов. \nПопробуйте еще раз 🛟",
                                reply_markup=get_cancel_kb())


@my_disp.callback_query_handler(state=BotStates.expensive_from_city_confirm, text="confirm")
async def from_city_confirm(callback_data: types.CallbackQuery):
    """Функция колбек хендлер, принимает подтверждение выбора города вылета"""
    await callback_data.answer(text="Вы подтвердили город вылета!")

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="🌀 Теперь напишите город, куда вы хотите лететь 🌀")

    await BotStates.expensive_to_city_wait.set()


@my_disp.message_handler(lambda message: message.text, state=BotStates.expensive_to_city_wait)
async def to_city(message: types.Message, state: FSMContext):
    """Функция хендлер принимает и записывает город назначения"""

    check_res = check_city(city_name=message.text)
    async with state.proxy() as data:
        data["to_city"] = check_res[0]
        to_city_iata = DBMethods.get_city_iata(city_name=check_res[0], language=check_res[1])
        if to_city_iata:
            data["to_city_iata"] = to_city_iata[0]
            await my_bot.send_message(chat_id=message.from_user.id,
                                      text=f"\n🛫 Вы летите в город <b>{data['to_city']}</b> 🛫"
                                           f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР ГОРОДА НАЗНАЧЕНИЯ</b>",
                                      parse_mode="HTML",
                                      reply_markup=get_confirm_ikb())
            await BotStates.expensive_to_city_confirm.set()

        else:
            await message.reply(text="Вы ввели город не корректно либо в нем нет аэропортов. \nПопробуйте еще раз 🛟",
                                reply_markup=get_cancel_kb())


@my_disp.callback_query_handler(state=BotStates.expensive_to_city_confirm)
async def to_city_confirm(callback_data: types.CallbackQuery):
    """Функция хендлер коллбека принимает подтверждение выбора города назначения"""
    await callback_data.answer(text="Вы подтвердили город вылета!")

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="🌀 Давайте сразу найдем обратные билеты? 🌀",
                                   reply_markup=get_return_ikb())

    await BotStates.expensive_return.set()


@my_disp.callback_query_handler(state=BotStates.expensive_return)
async def return_choose(callback_data: types.CallbackQuery, state: FSMContext):
    """Функция хендлер коллбека принимающая решение пользователя об обратном рейсе"""

    async with state.proxy() as data:
        data["return"] = callback_data.data

    await callback_data.answer(text="Ваш ответ принят!")
    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="Укажите дату начала периода, от когда нужно искать билеты",
                                   reply_markup=get_month_ikb())
    await BotStates.expensive_start_period_month.set()


@my_disp.callback_query_handler(state=BotStates.expensive_start_period_month)
async def get_start_month(callback_data: types.CallbackQuery, state: FSMContext):
    """Функция колбек хендлер, принимает месяц начала периода поиска билетов"""
    async with state.proxy() as data:
        data["start_date"] = callback_data.data

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="Теперь выберите точную дату",
                                   reply_markup=get_date_ikb(month=data["start_date"][5:]))
    await BotStates.expensive_start_period_date.set()


@my_disp.callback_query_handler(state=BotStates.expensive_start_period_date)
async def get_start_date(callback_data: types.CallbackQuery, state: FSMContext):
    """Функция колбек хендлер, принимает дату начала периода поиска билетов"""
    async with state.proxy() as data:
        data["start_date"] = f"{data['start_date']}-{callback_data.data}"

    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="Теперь выберите период, "
                                        "в течении которого от выбранной даты вы бы хотели вылететь",
                                   reply_markup=get_periods_ikb())
    await BotStates.expensive_period_choose.set()


@my_disp.callback_query_handler(state=BotStates.expensive_period_choose)
async def get_period(callback_data: types.CallbackQuery, state: FSMContext):
    """Функция колбек хендлер, принимает период поиска билетов
    Удаляет предыдущее сообщение и присылает список билетов
    Записывает в историю результаты поиска"""
    await callback_data.message.delete()

    async with state.proxy() as data:
        data["period"] = callback_data.data
        data["curr_ticket"] = 0

    tickets_bundle = ApiMethods.get_expensive_tickets(from_city=data["from_city_iata"],
                                                      to_city=data["to_city_iata"],
                                                      date=data["start_date"],
                                                      period=data["period"],
                                                      one_way=data["return"])
    async with state.proxy() as data:
        data["tickets_count"] = len(tickets_bundle)
        print("Колво билетов", data["tickets_count"])
        data["tickets_bundle"] = tickets_bundle

    if data["tickets_count"] > 1:
        await my_bot.send_message(chat_id=callback_data.from_user.id,
                                  text=get_listing_text(data=data,
                                                        tickets_bundle=tickets_bundle),
                                  parse_mode="HTML",
                                  reply_markup=get_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

        result_text = "".join(str(tickets_bundle))
        await BotStates.expensive_tickets_review.set()
    elif data["tickets_count"] == 1:
        await my_bot.send_message(chat_id=callback_data.from_user.id,
                                  text=get_listing_text(data=data,
                                                        tickets_bundle=tickets_bundle),
                                  parse_mode="HTML",
                                  reply_markup=get_small_tickets_ikb(link=tickets_bundle[data["curr_ticket"]]['gate']))

        result_text = "".join(str(tickets_bundle))
        await BotStates.expensive_tickets_review.set()
    else:
        await my_bot.send_message(chat_id=callback_data.from_user.id,
                                  text="Билеты не найдены. Попробуйте найти самостоятельно на aviasales.com",
                                  reply_markup=get_menu_kb())

        result_text = None
        await state.finish()

    DBMethods.add_result(conn=history_db_connect, user_id=callback_data.from_user.id,
                         command_type="Самые дорогие билеты", city_from=data["from_city"], city_to=data["to_city"],
                         start_date=data["start_date"], period=data["period"], return_fly=data["return"],
                         results=result_text)


@my_disp.callback_query_handler(state=BotStates.expensive_tickets_review, text=">>")
async def expensive_next_ticket(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["curr_ticket"] + 1 > data["tickets_count"] - 1:
            data["curr_ticket"] = 0
        else:
            data["curr_ticket"] += 1

    await callback_data.answer(text="Следующий билет!")
    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text=get_listing_text(data=data,
                                                         tickets_bundle=data["tickets_bundle"]),
                                   parse_mode="HTML",
                                   reply_markup=get_tickets_ikb(
                                       link=data["tickets_bundle"][data["curr_ticket"]]['gate']))


@my_disp.callback_query_handler(state=BotStates.expensive_tickets_review, text="<<")
async def expensive_previous_ticket(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["curr_ticket"] - 1 < 0:
            data["curr_ticket"] = data["tickets_count"] - 1
        else:
            data["curr_ticket"] -= 1

    await callback_data.answer(text="Предыдущий билет!")
    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text=get_listing_text(data=data,
                                                         tickets_bundle=data["tickets_bundle"]),
                                   parse_mode="HTML",
                                   reply_markup=get_tickets_ikb(
                                       link=data["tickets_bundle"][data["curr_ticket"]]['gate']))







