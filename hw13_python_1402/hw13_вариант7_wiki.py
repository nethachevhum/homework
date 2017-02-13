#Не знал, что имелось в виду: текст статьи или статься в html. Подумал, что для задания лучше подходит обычный текст,
#скопировал его.

import re


def gettext():
    f = open("1.txt",'r',encoding="utf8")
    ar = f.read()
    f.close()
    return ar

def repl(text): #непонятно, как сделать сохранение регистра первой буквы более изящным
    s1 = re.sub("Птиц(|а|ы|у|е|ей|ам|ами|ах)","Рыб\\1",(re.sub("птиц(|а|ы|у|е|ей|ам|ами|ах)","рыб\\1",text)))
    return(s1)

def savetext(text):
    f = open("2.txt","w",encoding="utf8")
    f.write(text)
    f.close()

def main():
    savetext(repl(gettext()))

if __name__ == "__main__":
    main()
