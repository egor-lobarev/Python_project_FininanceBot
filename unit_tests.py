import pandas as pd
import pytest

import finance_bot

# это я начал писать тесты на unittest
'''
class TestFinanceBot(unittest.TestCase):
    def test_empty_init(self):
        sample = finance_bot.FinanceBot()
        self.assertEqual([], sample.get_revenue_categories())
        self.assertEqual([], sample.get_expense_categories())
        self.assertEqual(type({}), type(sample.data))
        self.assertEqual(['expense/revenue(0/1)', 'value', 'date', 'category'], list(sample.data.keys()))
    def test_default_init(self):
        sample = finance_bot.FinanceBot(True, True)
        self.assertEqual(finance_bot.default_expense_categories, sample.expense_categories)
        self.assertEqual(finance_bot.default_revenue_categories, sample.revenue_categories)
        print(sample)
'''


class TestFinanceBot:
    def test_empty_init(self):
        sample = finance_bot.FinanceBot()
        assert sample.revenue_categories == []
        assert sample.expense_categories == []
        assert ['expense/revenue(0/1)', 'value', 'date', 'category'] == list(sample.data.keys())
        assert isinstance(sample.data, dict)

    def test_default_init(self):
        sample = finance_bot.FinanceBot(True, True)
        assert sample.revenue_categories == finance_bot.default_revenue_categories
        assert sample.expense_categories == finance_bot.default_expense_categories
        assert len(sample.data['date']) == finance_bot.ROWS_GENERATING

    def test_getters(self):
        sample = finance_bot.FinanceBot(True, True)
        assert sample.get_expense_categories() == sample.expense_categories
        assert sample.get_revenue_categories() == sample.revenue_categories

    def test_setters(self):
        sample = finance_bot.FinanceBot(False, False)
        with pytest.raises(Exception):
            sample.add_data(False, 'not_a_category', 1230)
        sample.add_category('маркет', False)
        assert ('маркет' in sample.get_expense_categories())
        sample.add_category('зарплата', True)
        assert ('зарплата' in sample.get_revenue_categories())
        sample.add_data(False, 'маркет', 1300)
        assert sample.data['value'][0] == 1300
        assert sample.data['category'][0] == 'маркет'
        sample.add_data(True, 'зарплата', 10000)
        assert sample.data['value'][1] == 10000
        assert sample.data['category'][1] == 'зарплата'
        with pytest.raises(Exception):
            sample.add_data(True, 'no_such_category', 1222)
    def test_save_read(self):
        sample = finance_bot.FinanceBot(True, True)
        sample.save_data('test_data')
        data_frame = pd.read_csv('test_data.csv')
        data_frame['date'] = pd.to_datetime(data_frame['date'])
        data = data_frame.to_dict('list')
        assert data == sample.data

        sample.read_data('test_data')
        assert sample.data == data
    def test_read(self):
        sample = finance_bot.FinanceBot(True, True)

if __name__ == '__main__':
    pytest.main()
