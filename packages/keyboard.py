from telebot.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType


class Button:
    def __init__(self, text, payload=None):
        self.text = text
        self.payload = payload


class Keyboard:
    def __init__(self, buttons_list):
        self.tg = ReplyKeyboardMarkup(resize_keyboard=True)
        for i in buttons_list:
            self.create_row(i)

    def create_row(self, row_list):
        self.tg.row(*[self.create_button(i) for i in row_list])

    def create_button(self, button):  # convert Button to KeyboardButton
        if button.payload:
            return KeyboardButton(button.text,
                                  request_poll=KeyboardButtonPollType(button.payload))
        return KeyboardButton(button.text)

    def get(self, messenger):
        if messenger == "telegram":
            return self.tg
        else:
            return None
