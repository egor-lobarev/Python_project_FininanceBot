from telebot.async_telebot import AsyncTeleBot

import telegram_config
import replies

bot = AsyncTeleBot(telegram_config.TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, replies.HELLO)