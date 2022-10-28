import datetime
import sqlite3db
from settings import DB_FILE

db = sqlite3db.SQLite3DataBase(DB_FILE)

days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')


def check_weekday(func):  # decorator
    def wrapper(*args, **kwargs):
        if args[3].weekday() == 6:  # args[3] = date
            args[0].message(args[1], "В этот день пар нет")  # args[0] = messenger; args[1] = id
        else:
            return func(*args, **kwargs)

    return wrapper


def message_schedule(messenger, id, lessons):
    if len(lessons) > 0:
        for lesson in lessons:
            messenger.message(id,
                              f"{lesson[0]}\n{lesson[1]}\n{lesson[2]}\n{lesson[3]}\n{lesson[5]}\n{lesson[4]}\n{lesson[6]}")
    else:
        messenger.message(id, 'Отсутствуют пары в выбранный день')


@check_weekday
def get(messenger, id, group, date):
    weekday = days[date.weekday()]
    req = db.get(group.upper(), weekday, (int(date.strftime("%V"))) % 2)
    message_schedule(messenger, id, req)


@check_weekday
def get_auditorium(messenger, id, auditorium, date):
    weekday = days[date.weekday()]
    req = db.get_auditorium(auditorium, weekday, (int(date.strftime("%V"))) % 2)
    message_schedule(messenger, id, req)


from packages.keyboard import Keyboard, Button


@check_weekday
def get_teacher(messenger, id, teacher, date, type_req=""):
    weekday = days[date.weekday()]
    req = db.get_teachers_by_name(teacher)
    if len(req) == 0:
        messenger.message(id, "Не знаю такого преподователя")
    elif len(req) > 1:
        keyboard = Keyboard([[Button(i[0], f"teacher {type_req}{i[0]}")] for i in req], is_inline=True)
        messenger.message(id, "Не совсем понял, кто имелся ввиду?",
                          keyboard=keyboard.get(messenger.get_type()))
    else:
        req = db.get_teacher(teacher, weekday, (int(date.strftime("%V"))) % 2)
        message_schedule(messenger, id, req)


@check_weekday
def get_teacher_call(messenger, id, teacher, date):
    weekday = days[date.weekday()]
    req = db.get_teacher_full_name(teacher, weekday, (int(date.strftime("%V"))) % 2)
    message_schedule(messenger, id, req)


def get_group_keyboard(**kwargs):
    group = kwargs['text'].split()[-1]
    keyboard = Keyboard([
        [Button(f"/расписание {group}")],
        [Button(f"/расписание завтра {group}")],
    ])
    kwargs["messenger"].message(kwargs["id"], f"Клавиатура группы {group}",
                                keyboard=keyboard.get(kwargs["messenger"].get_type()))


def auditorium_today(**kwargs):
    get_auditorium(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())


def auditorium_tomorrow(**kwargs):
    get_auditorium(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                   datetime.date.today() + datetime.timedelta(1))


def auditorium_after_tomorrow(**kwargs):
    get_auditorium(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                   datetime.date.today() + datetime.timedelta(2))


def auditorium_date(**kwargs):
    get_auditorium(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                   datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))


def schedule_today(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())


def schedule_tomorrow(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
        datetime.date.today() + datetime.timedelta(1))


def schedule_after_tomorrow(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
        datetime.date.today() + datetime.timedelta(2))


def schedule_date(**kwargs):
    get(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
        datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))


def teacher_today(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1], datetime.date.today())


def teacher_tomorrow(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                datetime.date.today() + datetime.timedelta(1), type_req="tomorrow ")


def teacher_after_tomorrow(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                datetime.date.today() + datetime.timedelta(2), type_req="after tomorrow ")


def teacher_date(**kwargs):
    get_teacher(kwargs['messenger'], kwargs['from_id'], kwargs['text'].split()[-1],
                datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'), type_req=kwargs['text'].split()[1])


def teacher_today_call(**kwargs):
    get_teacher_call(kwargs['messenger'], kwargs['from_id'], kwargs['text'][8:], datetime.date.today())

def teacher_tomorrow_call(**kwargs):
    get_teacher_call(kwargs['messenger'], kwargs['from_id'], kwargs['text'][17:],
                     datetime.date.today() + datetime.timedelta(1))

def teacher_after_tomorrow_call(**kwargs):
    get_teacher_call(kwargs['messenger'], kwargs['from_id'], kwargs['text'][23:],
                     datetime.date.today() + datetime.timedelta(2))

def teacher_date_call(**kwargs):
    get_teacher_call(kwargs['messenger'], kwargs['from_id'], kwargs['text'][19:],
                     datetime.datetime.strptime(kwargs['text'].split()[1], '%d.%m.%Y'))


def group_keyboard(**kwargs):
    get_group_keyboard(**kwargs)


from packages.command import Command

commands = [
    Command(r'/клавиатура группы ([А-Яа-я]+)Z?-(\d+)', group_keyboard,
            "\n/клавиатура группы {группа} - возвращает клавиатуру для указанной группы\n"),
    Command(r'/расписание ([А-Яа-я]+)Z?-(\d+)', schedule_today,
            "/расписание {группа} - возвращает расписание указанной группы на текущий день\n"),
    Command(r'/расписание завтра ([А-Яа-я]+)Z?-(\d+)', schedule_tomorrow,
            "/расписание завтра {группа} - возвращает расписание указанной группы на завтра\n"),
    Command(r'/расписание послезавтра ([А-Яа-я]+)Z?-(\d+)', schedule_after_tomorrow,
            "/расписание послезавтра {группа} - возвращает расписание указанной группы на послезавтра\n"),
    Command(r'/расписание [0-9]{2}.[0-9]{2}.[0-9]{4} ([А-Яа-я]+)Z?-(\d+)', schedule_date,
            "/расписание {дата} {группа} - возвращает расписание указанной группы на указанную дату\n"),


    Command(r'/аудитория (^[#*&])?[0-9]{3}', auditorium_today,
            "/аудитория {аудитория} - возвращает расписание указанной аудитории на текущий день\n"),
    Command(r'/аудитория завтра (^[#*&])?[0-9]{3}', auditorium_tomorrow,
                "/аудитория завтра {аудитория} - возвращает расписание указанной аудитории на завтра\n"),
    Command(r'/аудитория послезавтра (^[#*&])?[0-9]{3}', auditorium_after_tomorrow,
                "/аудитория послезавтра {аудитория} - возвращает расписание указанной аудитории на послезавтра\n"),
    Command(r'/аудитория [0-9]{2}.[0-9]{2}.[0-9]{4} (^[#*&])?[0-9]{3}', auditorium_date,
                "/аудитория {дата} {аудитория} - возвращает расписание указанной аудитории на указанную дату\n"),


    Command(r'/препод [A-ЯЁ]([а-яё])+', teacher_today,
            "/препод {фамилия с большой буквы} - возвращает расписание указанного преподавателя на текущий день\n"),
    Command(r'/препод завтра [A-ЯЁ]([а-яё])+', teacher_tomorrow,
                "/препод завтра {фамилия с большой буквы} - возвращает расписание указанного преподавателя на завтра\n"),
    Command(r'/препод послезавтра [A-ЯЁ]([а-яё])+', teacher_after_tomorrow,
                "/препод послезавтра {фамилия с большой буквы} - возвращает расписание указанного преподавателя на послезавтра\n"),
    Command(r'/препод [0-9]{2}.[0-9]{2}.[0-9]{4} [A-ЯЁ]([а-яё])+', teacher_date,
                "/препод {дата} {фамилия с большой буквы} - возвращает расписание указанного преподавателя на указанную дату\n"),

]

commands_call = [
    Command(r'teacher [\S\s]+[\S]+', teacher_today_call),
    Command(r'teacher tomorrow [\S\s]+[\S]+', teacher_tomorrow_call),
    Command(r'teacher after tomorrow [\S\s]+[\S]+', teacher_after_tomorrow_call),
    Command(r'teacher [0-9]{2}.[0-9]{2}.[0-9]{4} [\S\s]+[\S]+', teacher_date_call),
]
