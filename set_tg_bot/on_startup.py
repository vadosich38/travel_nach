from db_methods import DBMethods
from db_methods.connections import history_db_connect


async def on_start_up(_):
    print("Бот запущен")

    try:
        DBMethods.create_history_table(conn=history_db_connect)
        print("База данных создана")
    except Exception as error_text:
        print("При создании БД возникла ошибка:", error_text)
