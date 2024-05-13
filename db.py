import os
from typing import Dict, List, Tuple, Any

import sqlite3

main_path = os.path.dirname(os.path.abspath(__file__))
print("Path to main.py:", main_path)

conn = sqlite3.connect("email.db")

cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def execute_select(sql: str):
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def execute_dml(sql: str):
    cursor.execute(sql)
    conn.commit()


def execute_insert(sql: str):
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.commit()
    if row:
        return row
    else:
        return None


def fetchall(table: str, columns: List[str]) -> list[dict[str, Any]]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open(os.path.join(main_path, "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='email'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    print("Initializing database...")
    main_path = os.path.dirname(os.path.abspath(__file__))
    print("Path to main.py:", main_path)
    _init_db()


check_db_exists()

if __name__ == '__main__':
    # check_db_exists()

    result = execute_select(
        "SELECT * FROM email where email_id='AAMkADBkMWZkNjg2LWIyZDQtNGFlNC1iZTdkLTU2ODhhMTkyNWI1YQBGAAAAAABfFQzlzIsJRqu94r2KiuDHBwBjeTBmaHr8Trm4JLENL6HaAAAAAAEMAAAof14wdm3XTY7DgFHNF5tIAAIkJTZXAAA='")
    print(result)
    if result:
        print("exists")
    else:
        print("not exists")

    # insert(table="email", column_values={"email_id": 'AAMkADBkMWZkNjg2LWIyZDQtNGFlNC1iZTdkLTU2ODhhMTkyNWI1YQBGAAAAAABfFQzlzIsJRqu94r2KiuDHBwBjeTBmaHr8Trm4JLENL6HaAAAAAAEMAAAof14wdm3XTY7DgFHNF5tIAAIkJTZXAAA=', "created": '2024-05-09 13:13:23', "checked": '2024-05-09 13:13:23'})

    result = execute_insert(
        "INSERT INTO email (email_id, created, checked) VALUES "
        "('AAMkADBkMWZkNjg2LWIyZDQtNGFlNC1iZTdkLTU2ODhhMTkyNWI1YQBGAAAAAABfFQzlzIsJRqu94r2KiuDHBwBjeTBmaHr8Trm4JLENL6HaAAAAAAEMAAAof14wdm3XTY7DgFHNF5tIAAIkJTZXAAA=', "
        "'2024-05-09 13:13:23', "
        "'2024-05-09 13:13:23') RETURNING id")
    if result:
        print(result[0])
        print(type(result[0]))
    else:
        print("not inserted")
