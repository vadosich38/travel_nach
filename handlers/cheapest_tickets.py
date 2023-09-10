from set_tg_bot.dispatcher import my_disp
from set_tg_bot.bot import my_bot
from states.states_class import BotStates
from processing.city_checker import check_city
from db_methods.db_airports_class import DBMethods
from keyboards.cancel_kb import get_cancel_kb
from keyboards.menu_kb import get_menu_kb
from keyboards.airports_choose_ikb import get_airports_ikb
from keyboards.confirm_ikb import get_confirm_ikb
from keyboards.dates_choose import get_month_ikb, get_date_ikb
from keyboards.return_ikb import get_return_ikb
from api_package.api_cheapests_ticket import get_cheapest_tickets

from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext


@my_disp.message_handler(lambda message: message.text, Text(equals="💸 Найти дешевые билеты 💸", ignore_case=False))
async def cmd_cheapest_regim(message: types.Message):
    await message.reply(text="<b>Давайте найдем дешевые билеты для вашего перелета 👀</b>\n\n"
                             "Из какого города вы летите? ✈️",
                        parse_mode='HTML',
                        reply_markup=get_cancel_kb())
    await BotStates.cheap_from_city_wait.set()


@my_disp.message_handler(lambda message: message.text,
                         Text(equals="💥 ВЕРНУТСЬЯ В ГЛАВНОЕ МЕНЮ 💥", ignore_case=False),
                         state=BotStates.cheap_from_city_wait)
async def cmd_cancel_from_city_wait(message: types.Message, state: FSMContext):
    await message.reply(text="Вы вернулись в главное меню", reply_markup=get_menu_kb())
    await state.finish()


@my_disp.message_handler(lambda message: message.text, state=BotStates.cheap_from_city_wait)
async def from_city(message: types.Message, state: FSMContext):
    check_res = check_city(city_name=message.text)
    async with state.proxy() as data:
        data["from_city"] = check_res[0]
    airports = DBMethods.get_airports(city_name=check_res[0], language=check_res[1])

    if not airports:
        await message.reply(text="Вы ввели город не корректно либо в нем нет аэропортов. \nПопробуйте еще раз 🛟",
                            reply_markup=get_cancel_kb())
    elif len(airports) == 1:
        await message.answer(text=f"В этом городе есть только один аэропорт.\n"
                                  f"\n🛫 Ваш аэропорт вылета: <b>{airports[0][0]}</b> 🛫"
                                  f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР АЭРОПОРТА</b>",
                             parse_mode='HTML',
                             reply_markup=get_confirm_ikb())
        async with state.proxy() as data:
            data['from_airport'] = airports[0]
            data['from_all_airports'] = False

        await BotStates.cheap_from_city_airport_confirm.set()
    else:
        await message.answer(text="🛬 Теперь выберите аэропорт из списка ниже 🛬",
                             reply_markup=get_airports_ikb(airports=airports))
        await BotStates.cheap_from_city_airport_choose.set()


@my_disp.callback_query_handler(state=BotStates.cheap_from_city_airport_choose)
async def from_airport_choose(callback_data: types.CallbackQuery, state: FSMContext):
    await callback_data.answer(text="Вы выбрали аэропорт!")

    async with state.proxy() as data:
        if callback_data.data == "!":
            data['from_all_airports'] = True
            message_text = "Все аэропорты"
        else:
            data['from_airport'] = callback_data.data
            data['from_all_airports'] = False
            message_text = data['from_airport']

    await my_bot.send_message(chat_id=callback_data.from_user.id,
                              text=f"\n🛫 Ваш аэропорт вылета: <b>{message_text}</b> 🛫"
                                   f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР АЭРОПОРТА</b>",
                              parse_mode='HTML',
                              reply_markup=get_confirm_ikb())

    await BotStates.cheap_from_city_airport_confirm.set()


@my_disp.callback_query_handler(state=BotStates.cheap_from_city_airport_confirm, text="confirm")
async def from_airport_confirm_to_city(callback_data: types.CallbackQuery):
    await callback_data.answer(text="Аэропорт вылета подтвержден!")
    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="🌀 Теперь напишите город, куда вы хотите лететь 🌀")

    await BotStates.cheap_to_city_wait.set()


@my_disp.message_handler(lambda message: message.text, state=BotStates.cheap_to_city_wait)
async def to_city(message: types.Message, state: FSMContext):
    check_res = check_city(city_name=message.text)
    async with state.proxy() as data:
        data["to_city"] = check_res[0]

    airports = DBMethods.get_airports(city_name=check_res[0], language=check_res[1])

    if not airports:
        await message.reply(text="Вы ввели город не корректно либо в нем нет аэропортов. \nПопробуйте еще раз 🛟",
                            reply_markup=get_cancel_kb())
    elif len(airports) == 1:
        await message.answer(text=f"В этом городе есть только один аэропорт.\n"
                                  f"\n🛫 Ваш аэропорт прилета: <b>{airports[0][0]}</b> 🛫"
                                  f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР АЭРОПОРТА</b>",
                             parse_mode='HTML',
                             reply_markup=get_confirm_ikb())

        async with state.proxy() as data:
            data['to_airport'] = airports[0]
            data['to_all_airports'] = False

        await BotStates.cheap_to_city_airport_confirm.set()
    else:
        await message.answer(text="🛬 Теперь выберите аэропорт из списка ниже 🛬",
                             reply_markup=get_airports_ikb(airports=airports))
        await BotStates.cheap_to_city_airport_choose.set()


@my_disp.callback_query_handler(state=BotStates.cheap_to_city_airport_choose)
async def to_airport_choose(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_data.data == "!":
            data['to_all_airports'] = True
            message_text = "Все аэропорты"
        else:
            data['to_airport'] = callback_data.data
            data['to_all_airports'] = False
            message_text = data['to_airport']

    await callback_data.answer(text="Вы выбрали аэропорт!")
    await my_bot.send_message(chat_id=callback_data.from_user.id,
                              text=f"\n🛫 Ваш аэропорт прилета: <b>{message_text}</b> 🛫"
                                   f"\n\n<b>ПОДТВЕРДИТЕ ВЫБОР АЭРОПОРТА</b>",
                              parse_mode='HTML',
                              reply_markup=get_confirm_ikb())

    await BotStates.cheap_to_city_airport_confirm.set()


@my_disp.callback_query_handler(state=BotStates.cheap_to_city_airport_confirm, text="confirm")
async def to_airport_confirm_to_city(callback_data: types.CallbackQuery):
    await callback_data.answer(text="Аэропорт прилета подтвержден!")
    await my_bot.edit_message_text(chat_id=callback_data.from_user.id,
                                   message_id=callback_data.message.message_id,
                                   text="🌀 Выберите месяц вылета 🌀",
                                   reply_markup=get_month_ikb())

    await BotStates.cheap_to_month_wait.set()


@my_disp.callback_query_handler(state=BotStates.cheap_to_month_wait)
async def to_month_choose(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if int(callback_data.data[5:]) <= 9:
            data["departure_month_req"] = f"0{int(callback_data.data[5:])+1}"
        else:
            data["departure_month_req"] = str(int(callback_data.data[5:]) + 1)
        data["departure_year"] = callback_data.data[:4]

        # print("161", data["departure_month_req"])

        data["departure_month"] = callback_data.data[5:]

    await callback_data.answer(text="Месяц выбран")

    await my_bot.edit_message_text(
        chat_id=callback_data.from_user.id,
        message_id=callback_data.message.message_id,
        text="Теперь выберите точную дату вылета",
        reply_markup=get_date_ikb(month=data["departure_month"]))

    await BotStates.cheap_to_dates_wait.set()


@my_disp.callback_query_handler(state=BotStates.cheap_to_dates_wait)
async def to_date_choose(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if int(callback_data.data) <= 9:
            data["departure_date_req"] = f"0{callback_data.data}"
        else:
            data["departure_date_req"] = callback_data.data

        # print("180", data["departure_date_req"])
        data["departure_date"] = callback_data.data

    await callback_data.answer(text="Дата выбрана")
    await my_bot.edit_message_text(
        chat_id=callback_data.from_user.id,
        message_id=callback_data.message.message_id,
        text="Хотите выбрать обратные билеты?",
        reply_markup=get_return_ikb()
    )

    await BotStates.cheap_return.set()


@my_disp.callback_query_handler(state=BotStates.cheap_return)
async def to_return_choose(callback_data: types.CallbackQuery, state: FSMContext):
    if callback_data.data == "without_return":
        await my_bot.edit_message_text(
            chat_id=callback_data.from_user.id,
            message_id=callback_data.message.message_id,
            text="Ищу подходящие билеты, ожидайте...")
        async with state.proxy() as data:
            data["return"] = False
            tickets = get_cheapest_tickets(data)

        for i_ticket in tickets[0]:
            if i_ticket["success"]:
                print(i_ticket)
                # print("Цена:", i_ticket["data"]["BCN"]["1"]["price"])
            # for i_key, i_value in i_ticket.items():
            #     if i_key == "error" or i_key == "None":
            #         break
            #     else:
            #         print(i_key, i_value)
            #         print("\n")
        #сначала сохранить результаты в БД, в переменную
        await state.finish()
    elif callback_data.data == "with_return":
        async with state.proxy() as data:
            data["return"] = True
            await BotStates.cheap_return_month_wait.set()
            await my_bot.edit_message_text(
                chat_id=callback_data.from_user.id,
                message_id=callback_data.message.message_id,
                text="Когда вы хотите лететь обратно?",
                reply_markup=get_month_ikb(month=int(data["departure_month"])+1)
            )


@my_disp.callback_query_handler(state=BotStates.cheap_return_month_wait)
async def from_month_choose(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if int(callback_data.data[5:]) <= 9:
            data["return_departure_month_req"] = f"0{int(callback_data.data[5:])+1}"
        else:
            data["return_departure_month_req"] = int(callback_data.data[5:]) + 1
        data["return_departure_year"] = callback_data.data[:4]
        # print("224", data["return_departure_month_req"])

        data["return_departure_month"] = callback_data.data[5:]

        same_month = False
        if data["return_departure_month"] == data["departure_month"]:
            same_month = True

    await callback_data.answer(text="Месяц выбран")
    # print("тут")
    # print(data["departure_date"])
    # print(data["return_departure_month"])
    await my_bot.edit_message_text(
        chat_id=callback_data.from_user.id,
        message_id=callback_data.message.message_id,
        text="Теперь выберите точную дату обратного вылета",
        reply_markup=get_date_ikb(month=data["return_departure_month"],
                                  date=int(data["departure_date"]),
                                  same_month=same_month))

    await BotStates.cheap_return_dates_wait.set()


@my_disp.callback_query_handler(state=BotStates.cheap_return_dates_wait)
async def to_date_choose(callback_data: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if int(callback_data.data) <= 9:
            data["return_departure_date_req"] = f"0{callback_data.data}"
        else:
            data["return_departure_date_req"] = callback_data.data

        # print("249", data["return_departure_date_req"])

        data["return_departure_date"] = callback_data.data

    await callback_data.answer(text="Дата выбрана")
    await my_bot.edit_message_text(
        chat_id=callback_data.from_user.id,
        message_id=callback_data.message.message_id,
        text="Ищу подходящие билеты, ожидайте...")
    tickets = get_cheapest_tickets(data)
    print(tickets)
    # сначала сохранить результаты в БД, в переменную

    # await my_bot.send_message(chat_id=callback_data.from_user.id,
    #                           text=)
    await state.finish()

