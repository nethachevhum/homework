import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def get_dbs():
    conn = sqlite3.connect('hittite.db')
    crsr = conn.cursor()
    conn2 = sqlite3.connect("words.db")
    crsr_words = conn2.cursor()
    crsr_words.execute("CREATE TABLE words(id INTEGER PRIMARY KEY,Lemma,Wordform,Glosses)")
    arr = [] #тут хранятся все строки исхожной БД
    for line in crsr.execute("select * from wordforms"):
        arr.append(line)
        crsr_words.execute("INSERT INTO words (Lemma, Wordform, Glosses) VALUES ('{}','{}','{}')".format(line[0],line[1],line[2]))
    conn2.commit()
    conn3 = sqlite3.connect("glosse.db")
    crsr_gloss = conn3.cursor()
    crsr_gloss.execute("CREATE TABLE glosses(id INTEGER PRIMARY KEY,Gloss,Meaning)")
    glosses = {}
    glossesnum = {}
    with open("results.txt","r",encoding="utf-8") as f:
        lines = f.read().split("\n")
        for line in lines:
            if not line.split(" — ")[0] in glosses:
                glosses[line.split(" — ")[0]] = line.split(" — ")[1]

    #вытаскивание всех глосс
    for line in arr:
        for el in line[2].split("."):
            if el.isupper():
                if not el in glosses:
                    glosses[el] = el
    for gloss in glosses:
        crsr_gloss.execute("INSERT INTO glosses (Gloss, Meaning) VALUES ('{}','{}')".format(gloss, glosses[gloss]))
        print(gloss)
    conn3.commit()

    glossids = {}
    for line in crsr_gloss.execute("select * from glosses"):
        if not line[1] in glossids:
            glossids[line[1]] = line[0]

    conn4 = sqlite3.connect("ids.db")
    crsr_ids = conn4.cursor()
    crsr_ids.execute("CREATE TABLE ids (id INTEGER PRIMARY KEY,idname,idgloss)")
    wordgloss = [] #это массив с ид слов и ид глосс
    for index, word in enumerate(arr):
        for el in word[2].split("."):
            if el.isupper():
                wordgloss.append([index+1,glossids[el]])
                crsr_ids.execute("INSERT INTO ids (idname, idgloss) VALUES ('{}','{}')".format(index+1, glossids[el]))
    print(glossids)
    # print(glss)
    print(arr)
    # print(arr)
    print(glosses)
    # for el in arr:
    #     crsr_words.execute("INSERT INTO words (Lemma, Wordform, Glosses) VALUES ('{}','{}','{}') ".format())
    print(wordgloss)

    conn4.commit()
    return wordgloss, glossids

    #не забыть коммит
    # print(conn)


def get_graphs(wordgloss, glossids):
    #сначала посчитаем частотность разных падежей
    upd_ids = {v: k for k, v in glossids.items()}
    cases = ["NOM","ACC","GEN","DAT","LOC","INSTR","ABL","DAT-LOC","VOC"]
    casefreq = {}
    for line in wordgloss:
        if upd_ids[line[1]] in cases:
            if not line[1] in casefreq:
                casefreq[line[1]] = 1
            else:
                casefreq[line[1]] += 1
    new_dct = {}
    for key in casefreq:
        new_dct[upd_ids[key]] = casefreq[key]
    xs = []
    ys = []
    labels = []
    # Order
    a=0
    for key in new_dct:
        a += 1
        xs.append(a)
        labels.append(key)
        ys.append(new_dct[key])
    # plt.bar(xs, ys)

    plt.bar(xs, ys, align='center')
    plt.xticks(xs, labels)
    plt.show()

crtg = get_dbs()
get_graphs(crtg[0],crtg[1])