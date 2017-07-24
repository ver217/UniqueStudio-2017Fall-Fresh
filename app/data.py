import os
import time
def submit(info):
    check_flag=check_type(info)
    if not check_flag:
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
    for key,value in info.items():
        if value==None:
            return 713
        elif (key=="grade" or key=="resume") and type(value)!=int:
            return 712
        elif type(value)!=str:
            return 712
    return 0
