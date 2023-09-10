import sqlite3 as sq


def get_connection_history_db() -> sq.Connection:
    conn = sq.connect("history.db")
    return conn


def get_connection_airports() -> sq.Connection:
    conn = sq.connect("airports_db.db")
    return conn
