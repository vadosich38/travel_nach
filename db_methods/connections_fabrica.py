import sqlite3 as sq


def get_connection_history_db() -> sq.Connection:
    """Метод создает и возвращает коннектор с базой данных исторических запросов пользователей"""
    conn = sq.connect("history.db")
    return conn


def get_connection_cities() -> sq.Connection:
    """Метод создает и возвращает коннектор с базой данных аэропортов и кодов IATA"""
    conn = sq.connect("iata_db.db")
    return conn
