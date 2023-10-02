import sqlite3 as sq
from .connections import cities_db_connect


class DBMethods:
    """Класс методов работы с базами данных"""
    @staticmethod
    def create_history_table(conn: sq.Connection) -> bool:
        """Функция создает таблицу БД с историей запросов"""
        cur = conn.cursor()
        # cur.execute("DROP TABLE IF EXISTS searches")
        cur.execute("""CREATE TABLE IF NOT EXISTS searches(
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        command_type TEXT,
                        city_from TEXT,
                        city_to TEXT,
                        start_date TEXT,
                        period TEXT,
                        return_fly TEXT,
                        min_price INTEGER,
                        max_price INTEGER,
                        results TEXT)""")
        return True

    @staticmethod
    def add_result(conn: sq.Connection, user_id: int, command_type: str,
                   city_from: str, city_to: str, start_date: str,
                   period: str, return_fly: str, results: str,
                   min_price: int = None, max_price: int = None) -> None:
        """Метод записывает в БД историю поисков пользователя, хранятся только последние 10 запросов
        для каждого пользователя"""
        cur = conn.cursor()

        total_user_lines = len(cur.execute(f"SELECT * FROM searches WHERE user_id = {user_id}").fetchall())
        if total_user_lines > 0:
            oldest_id = cur.execute(f"""SELECT id FROM searches ORDER BY id ASC LIMIT 1""").fetchone()[0]
            newest_id = cur.execute(f"""SELECT id FROM searches ORDER BY id DESC LIMIT 1""").fetchone()[0]
        else:
            oldest_id = None
            newest_id = 0

        if total_user_lines < 10:
            new_line_numm = newest_id + 1
            cur.execute("""INSERT INTO searches VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (new_line_numm, user_id,
                                                                                             command_type, city_from,
                                                                                             city_to, start_date,
                                                                                             period, return_fly,
                                                                                             min_price, max_price,
                                                                                             results))
        else:
            new_line_numm = newest_id + 1
            cur.execute("""UPDATE searches SET id = ?, user_id = ?, command_type = ?, city_from = ?, city_to = ?, 
                            start_date = ?, period = ?, return_fly = ?, min_price = ?, max_price = ?, results = ? 
                            WHERE id = ?""", (new_line_numm, user_id, command_type, city_from, city_to, start_date,
                                              period, return_fly, min_price, max_price, results, oldest_id))
        conn.commit()

    @staticmethod
    def get_user_searches(user_id: int, conn: sq.Connection) -> list:
        """Функция возвращает исторические запросы пользователя"""

        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM searches WHERE user_id = {user_id}""")

        searches = cur.fetchall()
        return searches

    @staticmethod
    def get_city_iata(city_name: str, language: str) -> str:
        """Функция обращения к БД, возвращает код IATA переданого города"""

        cur = cities_db_connect.cursor()
        if language == "Latin":
            cur.execute("""SELECT city_code FROM cities WHERE city_name LIKE(?)""", (city_name, ))
        elif language == 'Cyrillic':
            cur.execute("""SELECT city_code FROM cities WHERE city_name_ru LIKE(?)""", (city_name, ))

        return cur.fetchone()
