import commands
import os
import requests
import json

from urllib.parse import quote

from flask import Flask, request

import telebot
from telebot import types


#@bot.message_handler(commands=['start'])

BOT_TOKEN = '5025602703:AAFl0VXzQabU48GHf5wgJUzarNC39MbhpQI'
APP_NAME = 'urfutimetablebot'
bot = telebot.TeleBot(BOT_TOKEN)

lessons_url = 'https://urfu.ru/api/schedule/groups/lessons/'
current_group_id = ''
current_fio = ''

@bot.message_handler(commands=[commands.start])
def start(message):
    bot.send_message(message.chat.id, f"Добрый день. Тут есть такие команды как:\n" +
                                      f"/{commands.group} [Твоя группа] - выставляет группу \n" +
                                      f"/{commands.fio} [Твоё ФИО] - (для преподавателей) выставляет фио \n" +
                                      f"/{commands.twoWeeks} - (для студентов) расписание на ближайшие две недели")

@bot.message_handler(commands=[commands.group])
def group(message):
    group_name = message.text.split(' ')[1]
    group_request_url = 'https://urfu.ru/api/schedule/groups/suggest/?query=' + quote(''.join(group_name))
    response = requests.get(group_request_url)
    suggestions = response.json()['suggestions']

    with open('testing.json', 'w') as outfile:
        json.dump(suggestions, outfile)

        if suggestions:
            result = ""
            for group_id in suggestions:
                result += f"{group_id['value']}\n"
            current_group_id = result.split('\n')[0]
            bot.send_message(message.chat.id, f"{current_group_id} - текущая группа")

@bot.message_handler(content_types=['text'])
def handler(message):
    bot.send_message(message.chat.id, "Я тебя услышал. Как минимум.")


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