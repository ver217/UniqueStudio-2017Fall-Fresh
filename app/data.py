
def submit(info,resume):
    if not resume:
        return 711
    check_flag=check_type(info)
    if not check_flag:
        return check_flag
    return 0

def check_type(info):
    for key,value in info.items():
        if key == "resume":
            info.remove("resume")
            continue
        if value==None:
            return 713
        elif key=="grade" and type(value)!=int:
            return 712
        elif type(value)!=str:
            return 712
    return 0