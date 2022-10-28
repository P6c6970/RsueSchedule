import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

url = os.environ.get("URL")

DB_FILE = os.environ.get("DB_NAME")

VERSIA = "0.0.2"



# Telegram settings
from packages.messenger import MessengerTelegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
telegram_url = os.environ.get("TELEGRAM_URL")
telegram = MessengerTelegram(TELEGRAM_TOKEN)

def change_tg_webhook(telegram): # для смены сервера
    telegram.telegram.remove_webhook()
    telegram.telegram.set_webhook(url="{0}{1}".format(url, telegram_url))

# change_tg_webhook(telegram)