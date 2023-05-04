from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
from telebot import types
from telebot import TeleBot

import telegram_config
import replies
from finance_bot import FinanceBot

# bot = AsyncTeleBot(telegram_config.TOKEN)
bot = TeleBot(telegram_config.TOKEN)


# Define a function to ask the user a yes/no question with an inline keyboard
def ask_yes_no_question(chat_id, question):
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text='Да', callback_data='да')
    no_button = InlineKeyboardButton(text='Нет', callback_data='нет')
    keyboard.row(yes_button, no_button)
    bot.send_message(chat_id=chat_id, text=question, reply_markup=keyboard)


def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('/трата')
    button2 = types.KeyboardButton('/доход')
    button3 = types.KeyboardButton('/статистика')
    keyboard.add(button1, button2, button3)
    return keyboard


def revenue_key_board(chat_id):
    keyboard = ReplyKeyboardMarkup()
    for category in FinanceBot().get_revenue_categories(chat_id):
        button = KeyboardButton(category)
        keyboard.add(button)
    return keyboard


def expense_key_board(chat_id):
    keyboard = ReplyKeyboardMarkup()
    for category in FinanceBot().get_expense_categories(chat_id):
        button = KeyboardButton(category)
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, replies.HELLO)
    ask_yes_no_question(message.chat.id, replies.HELLO_DEF)


@bot.callback_query_handler(func=lambda call: call.data in ['да', 'нет'])
def handle(call):
    callback_data = call.data
    chat_id = call.message.chat.id

    if callback_data == 'да':
        FinanceBot().default_categories(chat_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        bot.send_message(chat_id, "Успешно добавлены категории по умолчанию!", reply_markup=menu_keyboard())

    else:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        keyboard = InlineKeyboardMarkup(row_width=3)
        for category in replies.EXPENCE_CATEGORIES:
            button = InlineKeyboardButton(text=category, callback_data=category)
            keyboard.add(button)
        keyboard.add(InlineKeyboardButton(text='<<Выход', callback_data='выход'))

        # Send message with inline keyboard
        bot.send_message(call.message.chat.id, 'Выберите категории трат, которые вас интересуют:',
                         reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data in replies.EXPENCE_CATEGORIES)
def category_expense_handler(call):
    FinanceBot().add_expense_category(call.message.chat.id, call.data)

    selected_category = FinanceBot().get_expense_categories(call.message.chat.id)

    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in replies.EXPENCE_CATEGORIES:
        if category not in selected_category:
            button = types.InlineKeyboardButton(text=category, callback_data=category)
            keyboard.add(button)
    keyboard.add(InlineKeyboardButton(text='<<Выход', callback_data='выход'))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'выход' and not FinanceBot().get_revenue_categories(
    call.message.chat.id))
def category_expense_exit(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None)

    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in replies.REVENUE_CATEGORIES:
        button = InlineKeyboardButton(text=category, callback_data=category)
        keyboard.add(button)
    keyboard.add(InlineKeyboardButton(text='<<Выход', callback_data='выход'))

    # Send message with inline keyboard
    bot.send_message(call.message.chat.id, 'Выберите категории доходов, которые вас интересуют:',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in replies.REVENUE_CATEGORIES)
def category_revenue(call):
    FinanceBot().add_revenue_category(call.message.chat.id, call.data)

    selected_category = FinanceBot().get_revenue_categories(call.message.chat.id)

    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in replies.REVENUE_CATEGORIES:
        if category not in selected_category:
            button = InlineKeyboardButton(text=category, callback_data=category)
            keyboard.add(button)
    keyboard.add(InlineKeyboardButton(text='<<Выход', callback_data='выход'))

    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data == 'выход' and FinanceBot().get_revenue_categories(call.message.chat.id))
def category_revenue_exit(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None)
    bot.answer_callback_query(callback_query_id=call.id, text='Успешно добавлены категории!')


@bot.callback_query_handler(func=lambda call: call.data == 'выход' and FinanceBot().get_revenue_categories(
    call.message.chat.id) and FinanceBot().get_expense_categories(call.message.chat.id))
def exit_categories(call):
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None)
    bot.send_message(call.message.chat.id, 'Настрока категорий завершена! Теперь можно приступить к работе.',
                     reply_markup=menu_keyboard())


@bot.message_handler(commands=['трата'])
def add_exp(message):
    bot.send_message(chat_id=message.chat.id, text="Выберите категорию",
                     reply_markup=expense_key_board(message.chat.id))
    bot.register_next_step_handler(message, get_exp_category)


def get_exp_category(message):
    bot.send_message(chat_id=message.chat.id, text="Введите сумму траты",
                     reply_markup=None)
    category = message.text
    bot.register_next_step_handler(message, get_exp_value, category)


def get_exp_value(message, category):
    value = message.text
    FinanceBot().add_data(message.chat.id, category, value)
    bot.reply_to(message, "Отлично, трата добавлена!")


@bot.message_handler(commands=['доход'])
def add_rev(message):
    bot.send_message(chat_id=message.chat.id, text="Выберите категорию",
                     reply_markup=revenue_key_board(message.chat.id))
    bot.register_next_step_handler(message, get_rev_category)


def get_rev_category(message):
    bot.send_message(chat_id=message.chat.id, text="Введите сумму дохода",
                     reply_markup=None)
    category = message.text
    bot.register_next_step_handler(message, get_value, category)


def get_value(message, category):
    value = message.text
    FinanceBot().add_data(message.chat.id, category, value)
    bot.reply_to(message, "Отлично, доход добавлен!")


bot.polling()
