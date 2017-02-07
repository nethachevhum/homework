import re

def gettext():
    f = open("1.txt",'r',encoding="utf8")
    ar = f.read()
    f.close()
    return ar


def splitting(s):
    s1 = re.sub("([А-Я]|род)\.","\\1&&&",s) #здесь указаны не все сокращения
    s1 = re.sub("(\.|!|\?)","\\1###",s1)
    ar = s1.split("###")
    for i in range(0,len(ar)):
        ar[i] = ar[i].replace("&&&",".")
    
    return ar

print("\n".join(splitting(gettext())))
