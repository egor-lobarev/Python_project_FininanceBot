from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Заполнение значений по умолчанию

default_expense_categories = list(['cупермаркеты', 'аптеки', 'еда вне дома', 'переводы', 'одежда', 'регулярные',
                                   'развлечения', 'здоровье'])
default_revenue_categories = list(['Зарплата', 'переводы', 'аренда', 'дивиденды'])

# генератор рандомных данных

# rng = np.random.default_rng()
# base = datetime.today()
# date_list = [base - timedelta(days=x) for x in range(30)]
# exp_rev = list(rng.integers(0, 2, 30))
# category = list()
# for x in exp_rev:
#     if x:
#         category.append(random.choice(default_revenue_categories))
#     else:
#         category.append(random.choice(default_expense_categories))
#
# data = pd.DataFrame.from_dict(
#     {'expense/revenue (0/1)': exp_rev,
#      'value': list(rng.integers(100, 10000, 30)),
#      'date': date_list,
#      'category': category})
#
# запись в csv
# data.to_csv('data.csv', index = False)

# чтение данных из csv
data = pd.read_csv('data.csv')
data['date'] = pd.to_datetime(data['date'])


###########################
class FinanceBot:
    def __init__(self, is_default: bool = True):
        self.data = pd.DataFrame(columns=['expense/revenue (0/1)', 'value', 'date', 'category'])
        self.expense_categories = ()
        self.revenue_categories = ()
        if is_default:
            self.expense_categories = default_expense_categories
            self.revenue_categories = default_revenue_categories
            self.data = data

    def add_expense_category(self, new_category: str) -> None:
        self.expense_categories.append(new_category)

    def add_revenue_category(self, new_category: str) -> None:
        self.revenue_categories.append(new_category)

    def add_category(self, new_category: str, is_revenue: bool):
        if is_revenue:
            self.revenue_categories.append(new_category)
        else:
            self.expense_categories.append(new_category)

    def add_data(self, is_revenue: bool, category: str, value: int,
                 date: datetime.date = datetime.today()):
        if category not in self.expense_categories:
            raise NotImplemented('No such category')
        df = pd.DataFrame(
            {'expense/revenue (0/1)': [is_revenue],
             'value': [value],
             'date': [date],
             'category': [category]})

        self.data.append(df, ignore_index=True)

    def show_statistics_period(self, is_revenue: int, begin: datetime.date = (datetime.today() - timedelta(days=30)),
                        end: datetime.date = datetime.today()):
        df = self.data[(self.data['date'].between(begin, end)) & (self.data['expense/revenue (0/1)'] == is_revenue)]
        sum_value = df.groupby('category')['value'].sum()
        categories = df['category'].unique()

        plt.pie(sum_value, labels=self.data['category'].unique(), autopct='%1.1f%%', pctdistance=0.85, explode=[0.05] * len(sum_value))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Поступления' if is_revenue else 'траты')
        plt.show()

    def show_statistics_last(self, is_revenue: int, delta: int):
        begin = datetime.today() - timedelta(delta)
        df = self.data[(self.data['date'] >= begin) & (self.data['expense/revenue (0/1)'] == is_revenue)]
        sum_value = df.groupby('category')['value'].sum()
        categories = df['category'].unique()

        plt.pie(sum_value, labels=categories, autopct='%1.1f%%', pctdistance=0.85, explode=[0.05] * len(sum_value))
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Поступления' if is_revenue else 'траты')
        plt.show()

    def save(self):
        data.to_csv('data.csv', index=False)

    def get_expenses_categories(self):
        return pd.Series(self.expense_categories)

    def get_revenues_categories(self):
        return pd.Series(self.revenue_categories)
    def show_data(self):
        print(data)


if __name__ == '__main__':
    print(data)
    fb = FinanceBot()
    fb.show_statistics(0)
    fb.show_statistics(1)У