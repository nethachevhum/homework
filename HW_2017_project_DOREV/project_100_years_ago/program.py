import html
import urllib.request
import urllib.parse
from flask import Flask
from flask import render_template, url_for, request, redirect
import re
from bs4 import BeautifulSoup
import json
import os
import requests

#oreview программы: многое не доделано, в некоторых местах я до сих пор не понимаю, откуда ошибки;
#видимо, это оттого, что я заранее не спланировал, как сделать все, что нужно.
#Поэтому много try-except.



app = Flask(__name__)
def get_dct_page(word):
    headers = {
        "Host": "www.dorev.ru",
        "Cookie": "XMMGETHOSTBYADDR213134210163=U1%3A+163.210.unused-addr.ncport.ru; XMMcms4siteUSER=1; XMMFREE=YES; XMMPOLLCOOKIE=XMMPOLLCOOKIE",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }
    #a = open("test.html",mode="w+",encoding="windows-1251")
    res = requests.get("http://www.dorev.ru/ru-index.html?s="+urllib.parse.quote(word.encode("windows-1251")), headers=headers)
    # adress = urllib.request.Request("http://www.dorev.ru/ru-index.html?s="+urllib.parse.quote(word.encode("windows-1251")),headers=headers)
    page = ""
    # print(adress)
    # with urllib.request.urlopen(adress) as iter:
    #     return iter.read().decode("windows-1251")
    return res.text

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def get_text(page):
    # tags = re.compile('<.*?>', re.DOTALL)
    # spaces = re.compile('\s{2,}', re.DOTALL)
    # clean = spaces.sub('',tags.sub("",page))
    # return clean
    soup = BeautifulSoup(page,'html.parser')
    data = soup.findAll(text=True)
    results = filter(visible, data)
    return [el.replace("\xa0"," ") for el in list(results) if not el in ["\n"," ","\xa0"]]

def get_entry(word):
    page = get_dct_page(word)
    # ent = re.findall("<font color=\"#004488\">.+?</font>",page)
    soup = BeautifulSoup(page,'html.parser')
    try:
        ent = soup.find("font",{'color':'#004488'}).text.replace("'","") #NB, что эта штука находит без еров. Их надо будет вручную добавлять
    except:
        ent = word
    return ent

# что касается прилагательных: можно сторить в особый файл, как только замечаем прилагательное или существительное.
# в формате: слово:POS,case,gender
# потом проходимся по списку: видим, ага, прилагательное и существительное; смотрим, что у нас уже есть в файле.
# если согласуется -- запускаем отдельную фукнцию.
# если нет -- чистим и добавляем текущее слово. Может, алгоритм неполон.
def write_to_file(st):
    #записывает json
    # dammit = UnicodeDammit(st)
    # print(dammit)
    new_st = json.dumps(st)
    f = open("iter.txt","r+",encoding="utf-8")
    f.write(new_st)
    f.close()

def ver_root(word):
    #программа принимает полную форму слова
    #выдает полную форму -- в корне исправлены буквы.
    with open("in.txt","w+",encoding="utf-8") as f:
        f.write(word)
    # m = Mystem()
    # full_analysis = m.analyze(word)
    os.system("mystem.exe " + "-cgi --format json in.txt itter.txt" + " output.html")
    full_analysis = ""
    with open("itter.txt","r+",encoding="utf-8") as f:
        full_analysis = json.loads(f.read())
    gr = full_analysis[0]["analysis"][0]["gr"].replace("|",",").replace("(","").replace(")","").replace("=",",").split(",")
    print(gr)
    print(full_analysis)
    write_to_file(full_analysis)
    # f = open("iter.txt","r+",encoding="utf-8")
    # f.write(full_analysis)
    # f.close()
    lemma = full_analysis[0]["analysis"][0]["lex"]
    print(lemma)
    oldie_word = get_entry(lemma)
    # теперь идея такая: проходим по НЕ-лемматизированному слову и одновременно по лемматизированному; заменияем то, что
    # может быть не одним и тем же
    new_word = [letter for letter in word]
    rng = len(oldie_word)
    if len(word) < len(oldie_word):
        rng = len(word)
    for i in range(0,rng):
        if word[i] in "ифе" and word[i] != oldie_word[i] and oldie_word[i].lower() in "ѣiѵѳ":
            new_word[i] = oldie_word[i]
    new_word_st = "".join(new_word)
    #функция добавления яти объединена с этой -- чтобы не вызывать майстем дважды
    if "S" in gr and ("дат" in gr or "пр" in gr) and word.endswith("е"):
        new_word_st = new_word_st[:-1] + "ѣ"
    return new_word_st

def add_i(word):
    new_word = ""
    for index, el in enumerate(word):
        if el == "и" and index < len(word)-1 and word[index+1] in "аоэиуыеёюя":
            new_word += "i"
        else:
            new_word += el
    return new_word

def bez(word):
    new_word = ""
    prs = ["бес","черес","чрес"]
    for pr in prs:
        if word[:len(pr)] == pr and word[len(pr)] not in "аоэиуыеёюя":
            return pr[:-1]+"з" + word[len(pr):]
    return word

def add_shva(word):
    if word[len(word)-1] in "бвгджзклмнпрстфхцчшщ":
        return word + "ъ"
    return word

def add_iya(word):
    if word[-2:] == "ые":
        return word[:-2] + "ыя"
    elif word[-2:] == "ие":
        return word[:-2] + "iя"


def oldify_word(word,iya):
    try:
        if not iya:
            return add_i(add_shva(bez(ver_root(word))))
        return add_i(add_iya(add_shva(bez(ver_root(word)))))
    except:
        return word


# def work_text(text):
    # хорошо тестить, сколько у нас слов в

def oldify_text(sent):
    #на входе -- строка
    new_sent = []
    with open("in_textie.txt","w+",encoding="utf-8") as f:
        f.write(sent)
    os.system("mystem.exe " + "-cgi --format json in_textie.txt textie.txt" + " output.html")
    # gr = full_analysis[0]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(",")
    sent_analysis = []
    with open("textie.txt","r+",encoding="utf-8") as f:
        sent_analysis = json.loads(f.read())
    words = []

    print(sent.split())
    for index, word in enumerate(sent.split()):
        iya = False
        print(sent_analysis)
        print(index)
        try:
            if "analysis" in sent_analysis[index]:
                #print(sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=", ",").split(","))
                print("test" + " ".join(sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(",")))
                if "A" in sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(","):
                    # print(sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(","))
                    print("work")
                    for ddt in [-2,2]:
                        print(ddt)
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+str(ddt))
                        # print(sent_analysis[index + ddt]["text"])
                        cas_agr = False
                        num_agr = False
                        if "analysis" in sent_analysis[index+ddt]:
                            grrr = sent_analysis[index+ddt]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(",")
                            cases = ["им", "род", "вин", "дат", "пр", "твор"]
                            nums = ["ед", "мн"]
                            if "S" in grrr:
                                print("Saya orang INDONESSSIA!!!")
                                #согласуем, если в неоднозначностях хоть что-то совпадает -- неточно, но это уже вина майстема
                                for case in cases:
                                    if case in grrr and case in sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(","):
                                        cas_agr = True
                                        print("ANDA MELAYU!!!")
                                        break
                                for num in nums:
                                    if num in grrr and num in sent_analysis[index]["analysis"][0]["gr"].replace("|", ",").replace("(", "").replace(")", "").replace("=",",").split(","):
                                        num_agr = True
                                        print("anda ikan hiu!!!!!!")
                                        break
                        if cas_agr and num_agr:
                            if "жен" in grrr and "мн" in grrr and "им" in grrr:
                                iya = True
                                print("Здесь будет согласование: "+word)
                                break
        except:
            continue
        words.append(oldify_word(word,iya))
    return " ".join(words)

def oldify_page(texts):
    return "\n".join([oldify_text(text) for text in texts])


@app.route("/")
def main_page():
    try:
        content = oldify_word(request.args["word"].lower(),False)
    except:
        content = "-"
    # content = oldify_word(request.args["word"].lower(),False)
    print(content)
    return render_template("index.html",content=content)

@app.route("/testie")
def test():
    content = [(1,"апрѣль","апрель"),(2,"апрѣль","апрель"),(3,"апрѣль","апрель"),(5,"апрѣль","апрель"),(6,"апрѣль","апрель"),(7,"апрѣль","апрель"),(8,"апрѣль","апрель"),(9,"апрѣль","апрель"),(10,"апрѣль","апрель")]
    try:
        res = request.args
        right = 0
        print(res)
        for key in res:
            if res[key] == 'True':
                right += 1
                print("work")
        stright = str(right) + "/" + str(len(content)) + " right answers"
    except:
        stright = "-"

    # print(res)

    return render_template("testie.html",content=content,res=stright)

@app.route("/oldie-site")
def oldified_lenta():
    return render_template("oldie_site.html", content=oldify_page(get_text(requests.get("http://lenta.ru").text)))
    #если не грузить сайт, можно потестить на этом: return render_template("oldie_site.html",content=oldify_page(["Маленькие девочки пьют пиво","Я вместе с ними"]))


#
if __name__ == "__main__":
    app.run(debug=True)

# print(add_i("представление"))

# print(get_entry("занимать"))

# print(get_text(requests.get("http://lenta.ru/").text))

# oldify_text(" ".join(get_text(requests.get("http://lenta.ru/").text)))
#давайте делать стрип внутри фукнции
# oldify_text("Красивые пароходы, девочки красивые, двери уродливые, пугала ужасные, вонючие кучи на дворе...")

print(oldify_page(get_text(requests.get("http://lenta.ru").text)))

# print(get_text(get_dct_page("вася")))

# extract_text(urllib.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read())


# print(bez("пупсик"))

# print(ver_root("святилищем"))
# print(oldify_word("бессоветсный"))
