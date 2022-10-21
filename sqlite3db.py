# -*- coding: utf-8 -*-
import sqlite3

class SQLite3DataBase:
    def __init__(self, name):
        self.name = name
        self.name_table = "Schedule"

    def connect_open(self):
        conection = sqlite3.connect(self.name)
        return conection

    def create(self, cursor):
        try:
            cursor.execute(f"""CREATE TABLE {self.name_table}
                    (name_group, day_week, type_week, time, lesson, teacher, auditorium, type_lesson)""")
        except:
            pass

    def set(self, name_group, day_week, type_week, time, lesson, teacher, auditorium, type_lesson):
        connection = self.connect_open()
        cursor = connection.cursor()
        self.create(cursor)
        cursor.execute(f"INSERT INTO `{self.name_table}` VALUES('{name_group}', '{day_week}', '{type_week}', '{time}', '{lesson}', '{teacher}', '{auditorium}', '{type_lesson}')")
        #cursor.execute(f"INSERT INTO `{self.name_table}` VALUES(`name_group`=`{name_group}`, `day_week`=`{day_week}`, `type_week`=`{type_week}`, `time`=`{time}`, `lesson`=`{lesson}`, `teacher`=`{teacher}`, `auditorium`=`{auditorium}`, `type_lesson`=`{type_lesson}`)")
        connection.commit()
        connection.close()

    def get(self, group, day_week, type_week):
        connection = self.connect_open()
        cursor = connection.cursor()
        self.create(cursor)
        cursor.execute(f"SELECT name_group, day_week, type_week, time, lesson, group_concat(teacher), auditorium, type_lesson FROM '{self.name_table}' WHERE day_week='{day_week}' AND type_week='{type_week}' AND name_group='{group}' GROUP BY time ORDER BY cast(time as INTEGER);")
        a = cursor.fetchall()
        connection.commit()
        connection.close()
        return a

    def get_auditorium(self, auditorium, day_week, type_week):
        connection = self.connect_open()
        cursor = connection.cursor()
        self.create(cursor)
        cursor.execute(f"SELECT group_concat(name_group), day_week, time, lesson, auditorium, teacher, type_lesson, type_week FROM '{self.name_table}' WHERE day_week='{day_week}' AND auditorium='{auditorium}' AND type_week='{type_week}' GROUP BY lesson, time ORDER BY cast(time as INTEGER)")
        a = cursor.fetchall()
        connection.commit()
        connection.close()
        return a

    def get_teacher(self, teacher, day_week, type_week):
        connection = self.connect_open()
        cursor = connection.cursor()
        self.create(cursor)
        cursor.execute(f"SELECT group_concat(name_group), day_week, time, lesson, auditorium, teacher, type_lesson, type_week FROM '{self.name_table}' WHERE day_week='{day_week}' AND type_week='{type_week}' AND teacher LIKE '%{teacher}%' GROUP BY lesson, time ORDER BY cast(time as INTEGER)")
        a = cursor.fetchall()
        connection.commit()
        connection.close()
        return a


    def clear(self):
        connection = self.connect_open()
        cursor = connection.cursor()
        self.create(cursor)
        cursor.execute(f'DELETE FROM `{self.name_table}`')
        connection.commit()
        connection.close()