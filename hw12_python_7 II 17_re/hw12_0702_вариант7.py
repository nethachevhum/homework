import re

def gettext():
    f = open("1.html",'r',encoding="utf8")
    ar = f.read()
    f.close()
    return ar

def findcode(st):
    reg = "(http://www-01\.sil\.org/iso639-3/documentation\.asp\?id=)([a-z][a-z][a-z])"
    matches = re.findall(reg,st)
    return matches[0][1]


def main():
    print("Код этого языка: "+findcode(gettext()))

if __name__ == "__main__":
    main()

