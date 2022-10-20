import datetime
import sqlite3db
db = sqlite3db.SQLite3DataBase("SQLDB.db")

days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')

def get(message, id, group, date):
    if date.weekday() == 6:
        message(id, "В этот день пар нет")
    else:
        weekday = days[date.weekday()]
        req = db.get(group, weekday, (int(date.strftime("%V"))) % 2)
        for lesson in req:
            message(id, f"{lesson[0]}\n{lesson[1]}\n{lesson[3]}\n{lesson[4]}\n{lesson[5]}\n{lesson[6]}\n{lesson[7]}")


def get_auditorium(message, id, auditorium, date):
    if date.weekday() == 6:
        message(id, "В этот день пар нет")
    else:
        weekday = days[date.weekday()]
        req = db.get_auditorium(auditorium, weekday, (int(date.strftime("%V"))) % 2)
        for lesson in req:
            message(id, f"{lesson[0]}\n{lesson[1]}\n{lesson[2]}\n{lesson[3]}\n{lesson[5]}\n{lesson[4]}\n{lesson[6]}")


def auditorium_today(**kwargs):
    get_auditorium(kwargs['message'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())

def schedule_today(**kwargs):
    get(kwargs['message'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())

def schedule_tomorrow(**kwargs):
    get(kwargs['message'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today() + datetime.timedelta(1))

def schedule_after_tomorrow(**kwargs):
    get(kwargs['message'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today() + datetime.timedelta(2))

def schedule_date(**kwargs):
    get(kwargs['message'], kwargs['from_id'], kwargs['text'].split()[-1], date = datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))


commands = [
    (r'/расписание ([А-Я]+)Z?-(\d+)', schedule_today, "\n/расписание {группа} - возвращает расписание указанной группы на текущий день\n"),
    (r'/расписание завтра ([А-Я]+)Z?-(\d+)', schedule_tomorrow, "/расписание завтра {группа} - возвращает расписание указанной группы на завтра\n"),
    (r'/расписание послезавтра ([А-Я]+)Z?-(\d+)', schedule_after_tomorrow, "/расписание послезавтра {группа} - возвращает расписание указанной группы на послезавтра\n"),
    (r'/расписание [0-9]{2}.[0-9]{2}.[0-9]{4} ([А-Я]+)Z?-(\d+)', schedule_date, "/расписание {дата} {группа} - возвращает расписание указанной группы на указанную дату\n"),
    (r'/аудитория (^[#*&])?[0-9]{3}', auditorium_today, "/аудитория {аудитория} - возвращает расписание указанной аудитории на текущий день\n"),
    ]