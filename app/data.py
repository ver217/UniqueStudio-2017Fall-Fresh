import os
import time
args_list=[
    "name",
    "sex",
    "college",
    "major",
    "grade",
    "area",
    "phone",
    "email",
    "group",
    "intro",
    "resume"
]
def submit(info):
    check_flag=check_type(info)
    if check_flag!=0:
        return check_flag
    return 0

def save_resume(resume):
    if not resume:
        return 711
    filename=resume.name+str(time.time()).replace('.','_')
    with open(filename,"w") as file:
        file.write(resume)
    return 0

def check_type(info):
    for i in args_list: 
        if i not in info:
            return 713
        key=i
        value=info[key]
        if (key=="grade" or key=="resume"):
            if type(value)!=int:
                print(key,value)
                return 712
        elif type(value)!=str:
            return 712
    return 0
