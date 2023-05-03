from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types

import telegram_config
import replies
from finance_bot import FinanceBot

bot = AsyncTeleBot(telegram_config.TOKEN)

# Define a function to ask the user a yes/no question with an inline keyboard
async def ask_yes_no_question(chat_id, question):
    keyboard = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text='Да', callback_data='да')
    no_button = types.InlineKeyboardButton(text='Нет', callback_data='нет')
    keyboard.row(yes_button, no_button)
    await bot.send_message(chat_id=chat_id, text=question, reply_markup=keyboard)

def read_categories(chat_id, number_of_categories: int, is_revenue: bool):
    for _ in range(number_of_categories):
        category = str(input())
        if len(category) == 0:
            print('Нельзя делать категории из пустого слова')
            continue
        self.finance_bot.add_category(category, is_revenue)

@bot.message_handler(commands=['start'])
async def welcome(message):
    await bot.reply_to(message, replies.HELLO)
    await ask_yes_no_question(message.chat.id, replies.HELLO_DEF)

@bot.callback_query_handler(func=lambda call: True)
async def handle(call):
    callback_data = call.data
    chat_id = callback_data.chat.id

    if callback_data == 'да':
        categories_default = True
        random_data = False
        await ask_yes_no_question(chat_id, replies.HELLO_RAND)
        if callback_data == 'да':
            random_data = True
            finance_bot = FinanceBot(categories_default, random_data)
        elif callback_data == 'нет':
            finance_bot = FinanceBot()
            print(
                'Добавим сначала категории для трат, напишите их количество. Далее название каждой категории пишите с новой строки')
            number_categories = int(self.__poll(list(map(str, [i for i in range(1, 101)]))))
            self.read_categories(number_categories, False)
            print('Теперь добавим категории для любых выших поступлений. Алгоритм тот же.')
            number_categories = int(input())
            self.read_categories(number_categories, True)
            print("Успех!")
    await bot.answer_callback_query(call.id)



asyncio.run(bot.polling())
