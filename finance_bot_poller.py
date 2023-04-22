import pandas as pd

from finance_bot import FinanceBot


class FinanceBotPoller:
    def __start(self):
        message = self.__poll(['1', '2', '3'])
        match message:
            case '1':
                print("Выберите категорию из списка")
                exp = self.finance_bot.get_expense_categories()
                print(exp)
                ind = int(input())
                category = exp[ind]
                print("Введите сумму траты")
                value = int(input())
                self.finance_bot.add_data(0, category, value)
                print("Готово")
                self.finance_bot.print_data()

            case '2':
                print("Выберите категорию из списка")
                rev = self.finance_bot.get_revenue_categories()
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
        print('Хотите воспользоваться категориями трат и поступлений по умолчанию?\n(да\нет)')
        match self.__poll(['да', 'нет']):
            case'да':
                categories_default = True
                random_data = False
                print('Хотите сгенеироравть данные рандомно?\n(да/нет)')
                if self.__poll(['да', 'нет']) == 'да':
                    random_data = True
                self.finance_bot = FinanceBot(categories_default, random_data)
            case 'нет':
                self.finance_bot = FinanceBot()
                print(
                    'Добавим сначала категории для трат, напишите их количество. Далее название каждой категории пишите с новой строки')
                number_categories = int(input())
                self.read_categories(number_categories, False)
                print('Теперь добавим категории для любых выших поступлений. Алгоритм тот же.')
                number_categories = int(input())
                self.read_categories(number_categories, True)
                print("Успех!")

    def __init__(self):
        self.finance_bot = None
        self.__hello()
        self.__show_menu()
        self.__start()

    @staticmethod
    def __unknown_message():
        print('Не понял вас, попробуйте ещё раз')

    def __poll(self, list_of_words: list) -> str:
        while True:
            message = input()
            if message in list_of_words:
                return message
            elif message == 'exit':
                self.exit()
                return ''
            else:
                self.__unknown_message()

    @staticmethod
    def __show_menu():
        print('Меню:\n1. Добавить трату\n2. Добавить поступление\n3. Статистика\nДля перехода введите номер пункта')

    def exit(self):
        self.finance_bot.save_data()
        print('Пока!')

    def stats(self):
        print('1. Статистика за последние 30 дней\n2. Статистика за последние x дней\n3. Статистика с _ по _\nДля перехода введите номер пункта')
        message = str(input())
        if message == '1':
            self.finance_bot.show_statistics(0)
            self.finance_bot.show_statistics(1)
        if message == '2':
            print('введите количество дней:')
            days_number = int(input())
            self.finance_bot.show_statistics(0, days=days_number)
            self.finance_bot.show_statistics(1, days=days_number)
        if message == '3':
            print('Введите дату начала периода и конца с новой строки в формате dd/mm/yyyy')
            begin = pd.to_datetime(str(input()), format="%d/%m/%Y")
            end = pd.to_datetime(str(input()), format="%d/%m/%Y")
            self.finance_bot.show_statistics(0, begin, end)
            self.finance_bot.show_statistics(1, begin, end)
