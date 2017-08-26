# -*- coding:utf-8 -*-
import os
import time
import pymysql
import aiomysql
from sanic.exceptions import ServerError
from sanic_mysql import SanicMysql
from app import app

mysql_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'uniquestudio',
    'db': 'submit_info',
    'charset': 'utf8mb4',
    'cursorclass': aiomysql.DictCursor,
    'autocommit': True
}

app.config.update(dict(MYSQL=mysql_config))

SanicMysql(app)

save_path = os.getcwd() + "/resume"

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


async def submit(info):
    check_flag = check_type(info)
    if check_flag:
        return check_flag
    try:
        result = await app.mysql.query(insert_cmd, tuple([info[x] for x in args_list]))
    except Exception as e:
        print(e)
        return None
    return result


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


async def get_info():
    val = await app.mysql.query(select_cmd)
    tmp = map(time2str, val)
    return tmp


async def get_resume(name):
    try:
        flag = await app.mysql.query(select_resume_cmd, name)
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
    except Exception as e:
        print(e)
        return 710
