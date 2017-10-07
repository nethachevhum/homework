import urllib.request
import re
import os

def get_page(adress):
    try:
        raw = urllib.request.urlopen(adress)
        htmlp = raw.read().decode("utf-8")
        return htmlp
    except:
        print("page {} do not exist".format(adress))
        return

def get_adresses(): #эта функция достает все адреса номеров журнала
                    #адреса записываются в отдельный файл -- если они там есть,
                    #то новое извлечение ссылок не происходит
    main_page = urllib.request.urlopen("http://magazines.russ.ru/volga/").read().decode("ISO-8859-1")
    numbers = re.findall("volga/.*/[0-9][0-9]?[0-9]?(?:-[0-9][0-9]?)?",main_page)
    all_adresses = []
    adress_stack_raw = open("adresses.txt",encoding="utf-8")
    adress_stack = adress_stack_raw.readlines()
    adress_stack_raw.close()
    if len(adress_stack) < 3:
        print("adress file is empty, so we're searching again for page adresses")
        for number in numbers:
            try:
                num_page = urllib.request.urlopen("http://magazines.russ.ru/"+number).read().decode("ISO-8859-1")
                oeuvre_adress = re.findall(number+"/.*html",num_page)
                for el in oeuvre_adress:
                    all_adresses.append(el)
            except:
                print("error at {}".format(number))
        adress_stack_raw = open("adresses.txt","w+",encoding="utf-8")
        adress_stack_raw.write("\n".join(all_adresses))
        adress_stack_raw.close()
    return adress_stack    #адреса возвращаются в таком формате: volga/2017/1-2/moe-chastnoe-bessmertie.html


def clean_html(page,mode): #очищает html от тегов -- и еще сюда, по-моему, хорошо засунуть просто чистку от всего
                            #несколько режимов работы: text, author
    tags = re.compile("<.*?>", re.DOTALL)
    scripts = re.compile("<script>.*?</script>", re.DOTALL)
    comments = re.compile("<!--.*?-->", re.DOTALL)
    new_page = tags.sub("", scripts.sub("", comments.sub("", page)))
    if mode == "text":
        new_page = re.sub("\r", "",
                          re.sub("\n", " ", new_page)).replace("&nbsp;", "").replace("  ", "\n")
    elif mode == "author":
        new_page = re.sub("\r", "",
                          re.sub("\n", "", new_page)).replace("&nbsp;", "").replace("  ", "")
    new_page = new_page.replace("&#8230;","...").replace("&lt;","<").replace("&gt;",">")
    return new_page


def get_author_name(page):
    try:
        author = clean_html(re.findall('<div class="authors">.*?</div>',page,re.DOTALL)[0],"author")
        return author
    except:
        return ""

def get_header(page):
    try:
        header = clean_html(re.findall('<div class="col-xs-9">.*?<h1>(.*?)</h1>',page,re.DOTALL)[0],"text")
        return header
    except:
        return ""

def get_main_text(page,adress): #достает основной текст со страницы; NB, ЗДЕСЬ АДРЕС ТОЖЕ ДОЛЖЕН ПЕРЕДАВАТЬСЯ ПОЛНЫЙ!
    #       основной текст в блоке: <div class="body_contents">...</div>
    try:
        new_page = re.findall('<div class=Section1>(.*?)</div>',page,re.DOTALL)[0]
    except:
        try:
            new_page = re.findall('<div class=WordSection1>(.*?)</div>', page, re.DOTALL)[0]
        except:
            return
    new_page = clean_html(new_page,"text")
    month = re.findall("http://magazines.russ.ru/volga/.*?/(.*?)/",adress)[0]
    if month == "413":
        month = "7" #у них был особый номер -- они тогда надолго преркатили издание, думалось -- навсегда. Поэтому вместо месяца был написан номер вообще, за все время.
    st = "@au {}\n@ti {}\n@topic -\n@url {}@da ?.{}.{}".format(get_author_name(page),get_header(page),adress,month,re.findall("http://magazines.russ.ru/volga/([0123456789]+)/",adress)[0])
    new_page1 = st + "\n" + new_page
    return new_page, new_page1

def create_metadata(page,adress): #NB, что адрес должен быть в полной форме!
    month = re.findall("http://magazines.russ.ru/volga/.*?/(.*?)/", adress)[0]
    if month == "413":
        month = "7"
    year = re.findall("http://magazines.russ.ru/volga/([0123456789]+)/", adress)[0]
    name = re.findall("http://magazines.russ.ru/volga/.*?/.*?/(.*?)\.html", adress)[0]
    path = "./plain/{}/{}/{}".format(year,month,name)
    st = "{0}	{1}			{2}		публицистика					нейтральный	н-возраст	н-уровень" \
         "		{3}	Волга	{4}		литературный журнал	Россия	Саратов	ru".\
        format(path,get_author_name(page),get_header(page),
               adress,re.findall("http://magazines.russ.ru/volga/([0123456789]+)/",adress)[0])
    return st

def save_to_right_dir(text, adress): #mode -- это режим работы -- основная папка, в которую мы сохраняем: plain-xml_mystem-mystem
    if text == None:
        return
    mode = ["plain","mystem-xml","mystem-plain"]
    month = re.findall("http://magazines.russ.ru/volga/.*?/(.*?)/", adress)[0]
    if month == "413":
        month = "7"
    year = re.findall("http://magazines.russ.ru/volga/([0123456789]+)/",adress)[0]
    name = re.findall("http://magazines.russ.ru/volga/.*?/.*?/(.*?)\.html",adress)[0]
    for smode in mode:
        if not os.path.exists(os.path.join(os.path.dirname(__file__),smode,year,month)):
            os.makedirs(os.path.join(os.path.dirname(__file__),smode,year,month))
    f = open(os.path.join(os.path.dirname(__file__),mode[0],year,month,name+".txt"),"w+",encoding="utf-8")
    f.write(text[1])
    f.close()
    f1 = open(name+".txt","w",encoding="utf-8") #это "промежуточный" файл, который лежит в главной директории -- он нужен для того, чтобы майстем брал файл без "шапочки" с тегами
    f1.write(text[0])
    f1.close()
    os.system("mystem.exe " + "-di --format xml "+name+".txt " + mode[1] + os.sep + year + os.sep + month + os.sep + name +".xml")
    os.system("mystem.exe " + "-di "+name+".txt " + mode[
        2] + os.sep + year + os.sep + month + os.sep + name + ".txt")
    os.remove(name+".txt")

def main():
    print("I do work")
    save_to_right_dir(get_main_text(get_page("http://magazines.russ.ru/volga/2017/1-2/skvoz-kapli-na-stekle.html"),"http://magazines.russ.ru/volga/2017/1-2/skvoz-kapli-na-stekle.html"),"http://magazines.russ.ru/volga/2017/1-2/skvoz-kapli-na-stekle.html")
    st = ""
    for i,adress in enumerate(get_adresses()):
        print(adress)
        save_to_right_dir(
            get_main_text(get_page("http://magazines.russ.ru/"+adress),
                          "http://magazines.russ.ru/"+adress),
            "http://magazines.russ.ru/"+adress)
        st = st + create_metadata(get_page("http://magazines.russ.ru/"+adress),"http://magazines.russ.ru/"+adress) + "\n"
        print(st)
    m = open("metadata.csv","w+",encoding="utf-8")
    m.write(st)
    m.close()

if __name__ == "__main__":
    main()
