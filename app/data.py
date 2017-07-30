# -*- coding:utf-8 -*-
import os
import time
import pymysql
from sanic.exceptions import ServerError

save_path = os.getcwd() + "/resume"

mysql_config = {
    'user': 'root',
    'password': 'yyw19980424',
    'db': 'submit_info',
}

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': mysql_config['user'],
    'password': mysql_config['password'],
    'db': mysql_config['db'],
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

args_list = [
    "name",
    "sex",
    "major",
    "grade",
    "area",
    "phone",
    "email",
    "team",
    "intro",
    "resume"
]
xss_list = [
    '"',
    "'",
    ";",
    "\\",
    "/",
    "[",
    "]"
]

insert_cmd = "INSERT INTO info(" + "".join(
    [x + ',' for x in args_list[:-1]]) + "resume) VALUES(%s" + 9 * ",%s" + ");"

select_cmd = "SELECT * FROM info"

select_resume_cmd = "SELECT resume FROM info WHERE name=%s"


def db_setup():
    try:
        return pymysql.connect(**config)
    except Exception:
        raise ServerError("Can't connect to MySQL Server!", status_code=500)


def submit(info):
    connection = db_setup()
    check_flag = check_type(info)
    if check_flag:
        return check_flag
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_cmd,
                           tuple([info[x] for x in args_list]))
        connection.commit()
    finally:
        connection.close()
    return None


def save_resume(name, ext, resume):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if not resume:
        return 711
    filename = name + '_' + str(time.time()).replace('.', '_') + '.' + ext
    with open(os.path.join(save_path, filename), "wb") as file:
        file.write(resume)
    return None


def check_type(info):
    for i in args_list:
        if i not in info:
            return 713
        key = i
        value = info[key]
        if key == "grade" or key == "resume":
            if type(value) != int:
                return 712
        elif type(value) != str:
            return 712
        elif not defend_xss(value):
            return 714
    return None


def defend_xss(cmd):
    for i in xss_list:
        if i in cmd:
            return False
    return True


def time2str(element):
    element['lasttime'] = element['lasttime'].strftime("%Y/%m/%d - %H:%M:%S")
    return element


def get_info():
    connection = db_setup()
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_cmd)
            tmp = map(time2str, cursor.fetchall())
            result = tmp
        return result
    finally:
        connection.close()


def get_resume(name):
    connection = db_setup()
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_resume_cmd, name)
            flag = cursor.fetchone()
        if not flag:
            return None
        else:
            if not os.path.exists(save_path):
                return 715
            else:
                result = []
                for i in os.listdir(save_path):
                    if name in i:
                        result.append(i)
                if len(result):
                    return result
                return 716
    finally:
        connection.close()
