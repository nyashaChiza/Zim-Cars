
def ext_checker(name):
    if "." in name:        
        string = name.split(".")
        ext = string[1]
        if ext in [ 'png', 'jpg', 'jpeg','gif','jfif' ]:
            return True
        else:
            return False
    else:
        return False



print(not ext_checker("fff.pnhg"))