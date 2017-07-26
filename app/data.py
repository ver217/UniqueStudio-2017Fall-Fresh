import os
import time
from app import app

save_path = os.getcwd() + "/resume"

insert_cmd = "INSERT INTO info(name,sex,college,major,grade,area,phone,email,team,intro,resume) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

select_cmd = "SELECT * FROM info"

args_list = [
    "name",
    "sex",
    "college",
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


def submit(info):
    check_flag = check_type(info)
    if check_flag != 0:
        return check_flag
    with app.db.cursor() as cursor:
        cursor.execute(insert_cmd,
                       tuple(map(lambda x: x if type(x) == int else "'" + x + "'", [info[x] for x in args_list])))
    app.db.commit()
    return 0


def save_resume(resume):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if not resume:
        return 711
    filename = resume.name + str(time.time()).replace('.', '_')
    with open(os.path.join(save_path, filename), "w") as file:
        file.write(resume)
    return 0


def check_type(info):
    for i in args_list:
        if i not in info:
            return 713
        key = i
        value = info[key]
        if key == "grade" or key == "resume":
            if type(value) != int:
                print(key, value)
                return 712
        elif type(value) != str:
            return 712
        elif not defend_xss(value):
            return 714
    return 0


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
            result.append(tmp)
            tmp = cursor.fetchone()
    return result

# def get_resume():
