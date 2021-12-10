import os

import requests
import json

from urllib.parse import quote

from flask import Flask, request

import telebot
from telebot import types


BOT_TOKEN = '5025602703:AAFl0VXzQabU48GHf5wgJUzarNC39MbhpQI'
APP_NAME = 'urfutimetablebot'
bot = telebot.TeleBot(BOT_TOKEN)

lessons_url = 'https://urfu.ru/api/schedule/groups/lessons/'
current_group = ''
current_fio = ''

@bot.message_handler(content_types=['text'])
def handler(message):
    request_url = 'https://urfu.ru/api/schedule/groups/suggest/?query=' + quote(''.join(message.text))
    response = requests.get(request_url)
    suggestions = response.json()['suggestions']

    with open('testing.json', 'w') as outfile:
        json.dump(suggestions, outfile)

    bot.send_message(message.chat.id, "Я тебя услышал. Как минимум.")
    if suggestions:
        result = ""
        for group in suggestions:
            result += f"{group['value']}\n"
        bot.send_message(message.from_user.id, result)

if __name__ == '__main__':
    if "HEROKU" in list(os.environ.keys()):
        server = Flask(__name__)

        @server.route(f"/{BOT_TOKEN}", methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200

        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(
                url=f"https://{APP_NAME}.herokuapp.com/{BOT_TOKEN}")
            return "?", 200

        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))

    else:
        bot.remove_webhook()
        bot.polling()