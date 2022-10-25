from flask import Flask, request
from settings import telegram, telegram_url

app = Flask(__name__)

from telebot import types


@app.route('/{}'.format(telegram_url), methods=["POST"])
def webhook():
    telegram.telegram.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


@telegram.telegram.message_handler(commands=['start', 'help'])
def startCommand(message):
    processing.take_commands(messenger=telegram, id=message.chat.id, from_id=message.from_user.id, text="/помощь")


import processing


@telegram.telegram.message_handler(content_types='text')
def message_reply(message):
    try:
        id = message.chat.id
        from_id = message.from_user.id
        text = message.text

        if text != "":
            processing.take_commands(messenger=telegram, id=id, from_id=from_id, text=text)
    except Exception as e:
        telegram.message(id, e)


if __name__ == '__main__':
    app.run(debug=True)

"""

command.start()

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return '34b5a261'
    elif data['type'] == 'message_new':
        try:
            return 'ok'
        finally:
            command.main(data)
"""
