import re

def getar():
    f = open("1.txt",'r',encoding="utf8")
    ar = f.read().split()
    f.close()
    return ar

def normalize(ar):
    punct = "!?.,:;\'\"-—"
    arr = []
    for word in ar:
        word = word.strip("!?.,:;\«»'\"…-—()][*1234567890").lower()
        if word != "":
            arr.append(word)
    return arr


def findverb(ar):
    arr = []
    for word in ar:
        if re.match("(сиде?(л|ть|в|я))|(сиж(у|ива))|(сиди(те)?)",word):  #находит только формы гл. сидеть, без приставок.
            arr.append(word)                                            #search в этом случае не подходит: он находит и словас приставками
    return arr

def main():
    print(" ".join(findverb(normalize(getar()))))
    


if __name__ == "__main__":
    main()

