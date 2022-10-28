import datetime
import sqlite3db
db = sqlite3db.SQLite3DataBase("SQLDB.db")

days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')

def check_weekday(func): # decorator
    def wrapper(*args, **kwargs):
        if args[3].weekday() == 6: # args[3] = date
            args[0].message(args[1], "В этот день пар нет") # args[0] = messenger; args[1] = id
        else:
            return func(*args, **kwargs)
    return wrapper

@check_weekday
def get(messenger, id, group, date):
    weekday = days[date.weekday()]
    req = db.get(group, weekday, (int(date.strftime("%V"))) % 2)
    if len(req) > 0:
        for lesson in req:
            messenger.message(id, f"{lesson[0]}\n{lesson[1]}\n{lesson[3]}\n{lesson[4]}\n{lesson[5]}\n{lesson[6]}\n{lesson[7]}")
    else:
        messenger.message(id, 'Отсутствуют пары в выбранный день')

@check_weekday
def get_auditorium(messenger, id, auditorium, date):
    weekday = days[date.weekday()]
    req = db.get_auditorium(auditorium, weekday, (int(date.strftime("%V"))) % 2)
    if len(req) > 0:
        for lesson in req:
            messenger.message(id, f"{lesson[0]}\n{lesson[1]}\n{lesson[2]}\n{lesson[3]}\n{lesson[5]}\n{lesson[4]}\n{lesson[6]}")
    else:
        messenger.message(id, 'Отсутствуют пары в выбранный день')

@check_weekday
def get_teacher(messenger, id, teacher, date):
    weekday = days[date.weekday()]
    req = db.get_teacher(teacher, weekday, (int(date.strftime("%V"))) % 2)
    if len(req) > 0:
        for lesson in req:
            messenger.message(id, f"{lesson[0]}\n{lesson[1]}\n{lesson[2]}\n{lesson[3]}\n{lesson[5]}\n{lesson[4]}\n{lesson[6]}")
    else:
        messenger.message(id, 'Отсутствуют пары в выбранный день')



from packages.keyboard import Keyboard, Button
def get_group_keyboard(**kwargs):
    group = kwargs['text'].split()[-1]
    keyboard = Keyboard([
        [Button(f"/расписание {group}")],
        [Button(f"/расписание завтра {group}")],
        ])
    kwargs["messenger"].message(kwargs["id"], f"Клавиатура группы {group}", keyboard=keyboard.get(kwargs["messenger"].get_type()))

def auditorium_today(**kwargs):
    get_auditorium(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())

def schedule_today(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())

def schedule_tomorrow(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today() + datetime.timedelta(1))

def schedule_after_tomorrow(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today() + datetime.timedelta(2))

def schedule_date(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))

def teacher_today(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())

def teacher_tomorrow(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today() + datetime.timedelta(1))

def teacher_date(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))


def group_keyboard(**kwargs):
    get_group_keyboard(**kwargs)

from packages.command import Command
commands = [
    Command(r'/клавиатура группы ([А-Я]+)Z?-(\d+)', group_keyboard, "\n/клавиатура группы {группа} - возвращает клавиатуру для указанной группы\n"),
    Command(r'/расписание ([А-Я]+)Z?-(\d+)', schedule_today, "/расписание {группа} - возвращает расписание указанной группы на текущий день\n"),
    Command(r'/расписание завтра ([А-Я]+)Z?-(\d+)', schedule_tomorrow, "/расписание завтра {группа} - возвращает расписание указанной группы на завтра\n"),
    Command(r'/расписание послезавтра ([А-Я]+)Z?-(\d+)', schedule_after_tomorrow, "/расписание послезавтра {группа} - возвращает расписание указанной группы на послезавтра\n"),
    Command(r'/расписание [0-9]{2}.[0-9]{2}.[0-9]{4} ([А-Я]+)Z?-(\d+)', schedule_date, "/расписание {дата} {группа} - возвращает расписание указанной группы на указанную дату\n"),
    Command(r'/аудитория (^[#*&])?[0-9]{3}', auditorium_today, "/аудитория {аудитория} - возвращает расписание указанной аудитории на текущий день\n"),
    Command(r'/препод [A-ЯЁ]([а-яё])+', teacher_today, "/препод {фамилия с большой буквы} - возвращает расписание указанного преподавателя на текущий день\n"),
    Command(r'/препод завтра [A-ЯЁ]([а-яё])+', teacher_tomorrow, "/препод завтра {фамилия с большой буквы} - возвращает расписание указанного преподавателя на завтра\n"),
    Command(r'/препод [0-9]{2}.[0-9]{2}.[0-9]{4} [A-ЯЁ]([а-яё])+', teacher_date,
            "/препод {дата} {фамилия с большой букву} - возвращает расписание преподавателя на указанную дату\n"),

]