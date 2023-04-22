from datetime import datetime
from datetime import timedelta
import random

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Заполнение значений по умолчанию

default_expense_categories = list(['cупермаркеты', 'аптеки', 'еда вне дома', 'переводы', 'одежда', 'регулярные',
                                   'развлечения', 'здоровье'])
default_revenue_categories = list(['Зарплата', 'переводы', 'аренда', 'дивиденды'])
ROWS_GENERATING = 60
OPERATIONS_PER_DAY = 2
MIN_OPERATION = 100
MAX_OPERATION = 10000


###########################
class FinanceBot:
    def __init__(self, categories_default: bool = False, data_random: bool = False):
        self.data = {'expense/revenue(0/1)': [], 'value': [], 'date': [], 'category': []}
        self.expense_categories = []
        self.revenue_categories = []
        if categories_default:
            self.expense_categories = default_expense_categories
            self.revenue_categories = default_revenue_categories
            if data_random:
                self.data = self.__generate_data_randomly()

    def add_expense_category(self, new_category: str) -> None:
        self.expense_categories.append(new_category)

    def add_revenue_category(self, new_category: str) -> None:
        self.revenue_categories.append(new_category)

    def add_category(self, new_category: str, is_revenue: bool):
        if is_revenue:
            self.revenue_categories.append(new_category)
        else:
            self.expense_categories.append(new_category)

    def add_data(self, is_revenue: bool, category: str, value: int, date: datetime.date = datetime.today()):
        category_not_exists = category not in (self.revenue_categories if is_revenue else self.expense_categories)
        if category_not_exists:
            raise Exception('No such category')
        self.data['expense/revenue(0/1)'].append(is_revenue)
        self.data['value'].append(value)
        self.data['date'].append(date)
        self.data['category'].append(category)

    def show_statistics(self, is_revenue: int, begin: datetime.date = (datetime.today() - timedelta(days=30)),
                        end: datetime.date = datetime.today(), days: int = 0):
        data = pd.DataFrame(self.data)
        if days == 0:
            df = data[(data['date'].between(begin, end)) & (data['expense/revenue(0/1)'] == is_revenue)]
        else:
            df = data[(data['date'] >= (datetime.today() - timedelta(days=days))) & (
                    data['expense/revenue(0/1)'] == is_revenue)]
        sum_value = df.groupby('category')['value'].sum()
        categories = df['category'].unique()

        plt.pie(sum_value, labels=categories, autopct='%1.1f%%', pctdistance=0.85,
                explode=[0.05] * len(sum_value))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Поступления' if is_revenue else 'траты')
        plt.show()

    def save_data(self, filename: str = 'data'):
        pd.DataFrame(self.data).to_csv(filename + '.csv', index=False)

    def get_expense_categories(self) -> list:
        return self.expense_categories

    def get_revenue_categories(self) -> list:
        return self.revenue_categories

    def print_data(self):
        print(pd.DataFrame(self.data))

    def read_data(self, file_name: str = 'data'):
        frame = pd.read_csv(file_name + '.csv')
        frame['date'] = pd.to_datetime(frame['date'])
        self.data = frame.to_dict('list')

    @staticmethod
    def __generate_data_randomly() -> dict:
        rng = np.random.default_rng()
        base = datetime.today()
        date_list = [base - timedelta(days=x // OPERATIONS_PER_DAY) for x in range(ROWS_GENERATING)]
        exp_rev = list(rng.integers(0, 2, ROWS_GENERATING))
        category = list()
        for x in exp_rev:
            if x:
                category.append(random.choice(default_revenue_categories))
            else:
                category.append(random.choice(default_expense_categories))

        data = {'expense/revenue(0/1)': exp_rev,
                'value': list(rng.integers(MIN_OPERATION, MAX_OPERATION, ROWS_GENERATING)),
                'date': date_list,
                'category': category}

        return data


# чтение данных из csv
# data = pd.read_csv('data.csv')
# data['date'] = pd.to_datetime(data['date'])


if __name__ == '__main__':
    fb = FinanceBot()
    fb.print_data()
    fb.show_statistics(0)
    fb.show_statistics(1)