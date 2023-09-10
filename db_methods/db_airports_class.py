import sqlite3 as sq
from .connections import airports_db_connect
from processing.city_checker import check_city


class DBMethods:
    @staticmethod
    def create_table(conn: sq.Connection) -> bool:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS searches")
        cur.execute("""CREATE TABLE IF NOT EXISTS searches(
                        numm INT PRIMARY KEY NOT NULL,
                        city_from TEXT,
                        city_to TEXT,
                        date_from TEXT,
                        date_to TEXT,
                        results TEXT)""")
        return True

    @staticmethod
    def get_airports(city_name: str, language: str) -> tuple:
        cur = airports_db_connect.cursor()

        if language == 'Latin':
            cur.execute("""SELECT IATA FROM airports WHERE city LIKE(?)""", (city_name, ))
            return cur.fetchall()
        elif language == 'Cyrillic':
            cur.execute("""SELECT IATA FROM airports WHERE city_ru LIKE(?)""", (city_name, ))
            return cur.fetchall()
        else:
            raise Exception("Возникла ошибка при получении языка ввода!")
