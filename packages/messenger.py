import telebot


class MessengerTelegram:
    def __init__(self, TELEGRAM_TOKEN):
        self.telegram = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

    def message(self, id, text, keyboard=None):
        self.telegram.send_message(id, text, reply_markup=keyboard)

    @staticmethod
    def get_type():
        return "telegram"
