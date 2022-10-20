import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

url = os.environ.get("URL")

DB_FILE = "SQLDB.db"

VERSIA = "0.0.1"



# Telegram settings
import telebot




SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
telegram_url = os.environ.get("TELEGRAM_URL")
telegram = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
""" Одноразова для смены сервера
import time
telegram.remove_webhook()
time.sleep(1)
telegram.set_webhook(url="{0}{1}".format(url, telegram_url))

"""