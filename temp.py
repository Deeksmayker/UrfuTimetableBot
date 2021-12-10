import telebot

TOKEN = '5025602703:AAFl0VXzQabU48GHf5wgJUzarNC39MbhpQI'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "brrrrrr")

bot.polling()