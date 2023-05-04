import sqlite3
from sqlite3 import Error

#использую SQLite, чтобы не париться с созданием сервера в postreSQL. В первую очередь проверяющему)

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS data (
                                id serial,
                                expance_revenue bool,
                                value integer,
                                date text,
                                category text
                            );"""


class DataBaseConnection():
    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect('finance_bot.db')
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
            print()

    def add_row(self, a, b, c, d):


    def __del__(self):
        self.conn.close()

if '__name__' == '__main__':
    DataBaseConnection()