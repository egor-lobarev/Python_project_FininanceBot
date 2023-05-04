import sqlite3

sqlite_create_table_query1 = '''CREATE TABLE IF NOT EXISTS user (
                            id INTEGER PRIMARY KEY,
                            name INTEGER);'''

sqlite_create_table_query2 = '''CREATE TABLE IF NOT EXISTS operation (
                            id INTEGER REFERENCES user(id),
                            category TEXT NOT NULL,
                            date datetime,
                            value INTEGER,
                            PRIMARY KEY(id, date));'''

sqlite_create_table_query3 = '''CREATE TABLE IF NOT EXISTS revenue (
                            id INTEGER,
                            category INTEGER,
                            PRIMARY KEY(id, category));'''

sqlite_create_table_query4 = '''CREATE TABLE IF NOT EXISTS expense (
                            id INTEGER,
                            category INTEGER,
                            PRIMARY KEY (id, category));'''

sqlite_insert_expense_category = '''INSERT INTO expense VALUES (?, ?);'''
sqlite_insert_revenue_category = '''INSERT INTO revenue VALUES (?, ?);'''

sqlite_insert_operation = '''INSERT INTO operation VALUES (?, ?, ?, ?);'''

sqlite_insert_user = '''INSERT INTO user VALUES (?, ?)'''

sqlite_select_operations = '''SELECT category, date, value
                              FROM operation
                              WHERE date BETWEEN ? AND ? AND id = ?'''

sqlite_select_expenses = '''SELECT category
                            FROM expense
                            WHERE id = ?;'''
sqlite_select_revenues = '''SELECT category
                            FROM revenue
                            WHERE id = ?;'''


def create_database():
    sqlite_connection = sqlite3.connect('finance_bot_database.db')
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query1)
    cursor.execute(sqlite_create_table_query2)
    cursor.execute(sqlite_create_table_query3)
    cursor.execute(sqlite_create_table_query4)
