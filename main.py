from aiogram import executor
from set_tg_bot.on_startup import on_start_up
from db_methods.connections import history_db_connect, cities_db_connect

from handlers.cheapest_tickets import *
from handlers.history import *
from handlers.expensive_tickets import *
from handlers.diapason_tickets import *

if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher=my_disp,
                               on_startup=on_start_up,
                               skip_updates=True)
    except Exception as error_text:
        print("Возникла ошибка:", error_text)
    finally:
        history_db_connect.commit()
        history_db_connect.close()

        cities_db_connect.close()
