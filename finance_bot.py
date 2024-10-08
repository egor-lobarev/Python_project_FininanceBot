from datetime import datetime
from datetime import timedelta
import random

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3

import database
import replies

# Заполнение значений по умолчанию

default_expense_categories = replies.EXPENCE_CATEGORIES
default_revenue_categories = replies.REVENUE_CATEGORIES
ROWS_GENERATING = 60
OPERATIONS_PER_DAY = 2
MIN_OPERATION = 100
MAX_OPERATION = 10000


###########################
class FinanceBot:
    def __init__(self, categories_default: bool = False, data_random: bool = False):
        database.create_database()
        self.connection = sqlite3.connect('finance_bot_database.db')
        self.cursor = self.connection.cursor()

    def new_user(self, chat_id: int, name: str):
        try:
            self.cursor.execute(database.sqlite_insert_user, (chat_id, name))
            self.connection.commit()
        except:
            print("ашипка, нельзя второй пользователь такой же")

    def add_expense_category(self, chat_id: int, new_category: str) -> None:
        try:
            self.cursor.execute(database.sqlite_insert_expense_category, (chat_id, new_category))
            self.connection.commit()
        except:
            print("ашипка, низя вторую категориб добавлять")

    def add_revenue_category(self, chat_id: int, new_category: str) -> None:
        try:
            self.cursor.execute(database.sqlite_insert_revenue_category, (chat_id, new_category))
            self.connection.commit()
        except:
            print("ашипка, низя вторую категориб добавлять")

    def add_data(self, chat_id: int, category: str, value: int, date: datetime.date = datetime.today()):
        self.cursor.execute(database.sqlite_insert_operation, (chat_id, category, date, value))
        self.connection.commit()

    def get_users(self):
        self.cursor.execute(database.sqlite_select_users)
        data = self.cursor.fetchall()
        if data:
            return list(list(zip(*data))[0])
        return []

    def default_categories(self, chat_id: int):
        for exp in default_expense_categories:
            self.add_expense_category(chat_id, exp)
        for rev in default_revenue_categories:
            self.add_revenue_category(chat_id, rev)

    def show_statistics(self, chat_id: int, is_revenue: int,
                        begin: datetime.date = (datetime.today() - timedelta(days=30)),
                        end: datetime.date = datetime.today()):
        self.cursor.execute(database.sqlite_select_operations, (begin, end, chat_id))
        data = pd.DataFrame(self.cursor.fetchall(), columns=['category', 'date', 'value'])
        if is_revenue:
            self.cursor.execute(database.sqlite_select_revenues, (chat_id,))
        else:
            self.cursor.execute(database.sqlite_select_expenses, (chat_id,))
        list_categories = list(list(zip(*self.cursor.fetchall()))[0])
        df = data[(data['category'].isin(list_categories))]
        sum_value = df.groupby('category')['value'].sum()
        categories = sum_value.index

        plt.pie(sum_value, labels=categories, autopct='%1.1f%%', pctdistance=0.85,
                explode=[0.05] * len(sum_value))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Поступления' if is_revenue else 'траты')
        plt.savefig(f'stats{is_revenue}.png')
        plt.show()

    def get_expense_categories(self, chat_id: int) -> list:
        self.cursor.execute(database.sqlite_select_expenses, (chat_id,))
        data = self.cursor.fetchall()
        if data:
            return list(list(zip(*data))[0])
        return []

    def get_revenue_categories(self, chat_id: int) -> list:
        self.cursor.execute(database.sqlite_select_revenues, (chat_id,))
        data = self.cursor.fetchall()
        if data:
            return list(list(zip(*data))[0])
        return []

    # def print_data(self):
    #     print(pd.DataFrame(self.data))

    # def read_data(self, file_name: str = 'data'):
    #     frame = pd.read_csv(file_name + '.csv')
    #     frame['date'] = pd.to_datetime(frame['date'])
    #     self.data = frame.to_dict('list')

    def generate_data_randomly(self, chat_id: int):
        rng = np.random.default_rng()
        base = datetime.today()
        date_list = [base - timedelta(days=x // OPERATIONS_PER_DAY, seconds=x % OPERATIONS_PER_DAY) for x in
                     range(ROWS_GENERATING)]
        category = list()
        self.cursor.execute(database.sqlite_select_revenues, (chat_id,))
        revenue_categories = self.cursor.fetchall()
        self.cursor.execute(database.sqlite_select_expenses, (chat_id,))
        expense_categories = self.cursor.fetchall()
        categories = revenue_categories + expense_categories
        for _ in range(ROWS_GENERATING):
            category.append(random.choice(categories))
        values = list(map(int, rng.integers(MIN_OPERATION, MAX_OPERATION, ROWS_GENERATING)))

        for i in range(ROWS_GENERATING):
            self.cursor.execute(database.sqlite_insert_operation, (chat_id, category[i][0], date_list[i], values[i]))
        self.connection.commit()


    def reset_data(self, chat_id):
        #try:
            self.cursor.execute(database.sqlite_delete_user, (chat_id,))
            self.cursor.execute(database.sqlite_delete_operation, (chat_id,))
            self.cursor.execute(database.sqlite_delete_revenue, (chat_id,))
            self.cursor.execute(database.sqlite_delete_expense, (chat_id,))
            self.connection.commit()
        #except:
         #   print("Что-то пошло не так во время удаления")


# чтение данных из csv
# data = pd.read_csv('data.csv')
# data['date'] = pd.to_datetime(data['date'])


if __name__ == '__main__':
    fb = FinanceBot()
    fb.new_user(1, 'danya-loh')
    fb.add_data(1, 'jopa', 100)
    fb.add_expense_category(1, 'sds')
    fb.add_revenue_category(1, 'wewea')
    fb.add_expense_category(1, 'asdasf')
    fb.add_revenue_category(1, 'wkllk')
    fb.generate_data_randomly(1)
    fb.show_statistics(1, 0)
    fb.show_statistics(1, 1)
