import pandas as pd

from FinanceBot import FinanceBot

class finance_bot_poller:
    def __poll(self):
        while True:
            message = input()
            if message == 'exit':
                self.__exit()
                break
            match message:
                case '1':
                    print("Выберите категорию из списка")
                    exp = self.finance_bot.get_expenses_categories()
                    print(exp)
                    ind = int(input())
                    category = exp[ind]
                    print("Введите сумму траты")
                    value = int(input())
                    self.finance_bot.add_data(0, category, value)
                    print("Готово")
                    self.finance_bot.show_data()

                case '2':
                    print("Выберите категорию из списка")
                    rev = self.finance_bot.get_revenues_categories()
                    print(rev)
                    ind = int(input())
                    category = rev[ind]
                    print("Введите сумму поступления")
                    value = int(input())
                    self.finance_bot.add_data(1, category, value)
                    print("Готово")
                case '3':
                    self.stats()
            self.__show_menu()

    def read_categories(self, number_of_categories: int, is_revenue: bool):
        for _ in range(number_of_categories):
            category = str(input())
            if len(category) == 0:
                print('Нельзя делать категории из пустого слова')
                continue
            self.finance_bot.add_category(category, is_revenue)

    def __hello(self):
        print('Привет, я стану твоим персональным финансовым помощникм для отслеживания своих трат. Давай начнём!'
              'Если вы захотите завершить сессию, введите \'exit\'')
        print('Хотите воспользоваться категориями трат и поступлений по умолчанию? \n\
              Если что их всегда можно будет поменять!\n(да\нет)')
        message = str(input())
        if message == 'да':
            self.finance_bot = FinanceBot()
        elif message == 'нет':
            self.finance_bot = FinanceBot(False)
            print('Добавим сначала категории для трат, напишите их количество. Далее название каждой категории пишите с новой строки')
            number_categories = int(input())
            self.read_categories(number_categories, False)
            print('Теперь добавим категории для любых выших поступлений. Алгоритм тот же.')
            number_categories = int(input())
            self.read_categories(number_categories, True)
            print("Успех!")
        else:
            self.__unknown_message()

    def __init__(self):
        self.finance_bot = None
        self.__hello()
        self.__show_menu()
        self.__poll()

    @staticmethod
    def __unknown_message():
        print('Не понял вас, попробуйте ещё раз')

    @staticmethod
    def __show_menu():
        print('Меню:\n1. Добавить трату\n2. Добавить поступление\n3. Статистика\nДля перехода введите номер пункта')

    def __exit(self):
        self.finance_bot.save()
        print('Пока!')

    def stats(self):
        print('1. Статистика за последние 30 дней\n 2. Статистика за последние x дней\n 3. Статистика с _ по _\nДля перехода введите номер пункта')
        message = str(input())
        if message == '1':
            self.finance_bot.show_statistics_period(0)
            self.finance_bot.show_statistics_period(1)
        if message == '2':
            print('введите количество дней:')
            days_number = int(input())
            self.finance_bot.show_statistics_last(0, days_number)
            self.finance_bot.show_statistics_last(1, days_number)
        if message == '3':
            print('Введите дату начала периода и конца с новой строки в формате dd/mm/yyyy')
            begin = pd.to_datetime(str(input()), format="%d/%m/%Y")
            end = pd.to_datetime(str(input()), format="%d/%m/%Y")
            self.finance_bot.show_statistics_period(0, begin, end)
            self.finance_bot.show_statistics_period(1, begin, end)


