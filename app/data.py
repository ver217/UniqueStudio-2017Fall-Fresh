# -*- coding:utf-8 -*-
import os
import time
from app import app

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


def submit(info):
    check_flag = check_type(info)
    if check_flag:
        return check_flag
    with app.db.cursor() as cursor:
        cursor.execute(insert_cmd,
                       tuple([info[x] for x in args_list]))
    app.db.commit()
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


def get_info():
    result = []
    with app.db.cursor() as cursor:
        cursor.execute(select_cmd)
        tmp = cursor.fetchone()
        while tmp:
            print(tmp)
            tmp=list(tmp)
            tmp[-2]=tmp[-2].strftime("%Y/%m/%d - %H:%M:%S")
            result.append(tmp)
            tmp = cursor.fetchone()
    return result


def get_resume(name):
    with app.db.cursor() as cursor:
        cursor.execute(select_resume_cmd, name)
        flag = cursor.fetchone()
    if type(flag) != tuple:
        return None
    elif flag == 0:
        return None
    else:
        if not os.path.exists(save_path):
            return 715
        else:
            for i in os.listdir(save_path):
                if name in i:
                    return os.path.join(save_path, i)
            return 716
