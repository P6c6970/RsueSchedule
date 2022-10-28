from telebot.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Button:
    def __init__(self, text, payload=None):
        self.text = text
        self.payload = payload

    def get_tg(self, is_inline=False):  # convert Button to KeyboardButton or InlineKeyboardButton
        if is_inline:
            return InlineKeyboardButton(self.text,
                                        callback_data=self.payload if self.payload else self.text)
        if self.payload:
            return KeyboardButton(self.text,
                                  request_poll=KeyboardButtonPollType(self.payload))
        return KeyboardButton(self.text)


class Keyboard:
    def __init__(self, buttons_list, is_inline=False):
        self.is_inline = is_inline
        if self.is_inline:
            self.tg = InlineKeyboardMarkup()
        else:
            self.tg = ReplyKeyboardMarkup(resize_keyboard=True)
        for i in buttons_list:
            self.create_row(i)

    def create_row(self, row_list):
        self.tg.row(*[i.get_tg(self.is_inline) for i in row_list])

    def get(self, messenger):  # getting the keyboard for the desired messenger
        if messenger == "telegram":
            return self.tg
        return None

    @classmethod
    def delete_keyboard(cls, messenger):  # for removing the keyboard
        if messenger == "telegram":
            return ReplyKeyboardRemove()
        return None