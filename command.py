# -*- coding: utf-8 -*-
import re

command_text_list = None

def help_list(**kwargs):
    kwargs["message"](kwargs["id"], f"Вот команды которые я понимаю:\n{command_text_list}")

commands = [
    ('/помощь', help_list),
    ]

import plugins.schedule as schedule
commands += schedule.commands

command_text_list = '\n'.join([i[2] if len(i)>2 else i[0] for i in commands ])




def search_commands(command):
    for i in commands:
        if re.fullmatch(i[0], command):
            return i[1]


def take_commands(**kwargs):
    fun = search_commands(kwargs["text"])
    if fun is not None:
        fun(message=kwargs["message"], id=kwargs["id"], from_id=kwargs["from_id"], text=kwargs["text"])
    elif kwargs["id"]==kwargs["from_id"]:
        kwargs["message"](kwargs["id"], 'Ничего не понял')
#if re.fullmatch(regex_name, message):