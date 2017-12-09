from flask import Flask
from flask import render_template, url_for, request, redirect
import json
from concepts import Context
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/netkachev/Anaconda3/Library/bin/graphviz'

app = Flask(__name__)
#!!!!!

#идея сейчас такая: каждому языку соответствует key; каждому key -- value, который массив словарей со значениями.
#один фрейм могут покрывать несколько глаголов. При инпуте они разделяются знаком ;
#Когда программа запускается, она заходит в текстовый файл с уже записанными данными, и выгружает их.
#К выгруженным данным добавляется ввод пользователя; учитывается, что может быть несколько вводов для одного языка --
#для, например, таких случаев, когда разные информанты говорят разное.


def get_table():
    # file = open("relations.csv").read()
    # print(file)
    for file in os.listdir("graphs"):
        c = Context.fromfile("graphs"+os.sep+file,frmat="csv",encoding="utf-8")
        a = c.lattice.graphviz()
        a.format = "png"
        a.render("static"+os.sep+file[:-4]+'.gv')
        #теперь, видимо, нужно, чтобы:
            #сохранялось в папку static, чтобы это потом можно было выводить в html

def write_to_file(name,str):
    f = open("graphs"+os.sep+name+".csv","w",encoding="utf-8")
    f.write(str)
    f.close()

def format_data():
    #на выходе у нас должен быть массив из строк, которые можно записать в .csv в нужном формате
    f = open("out.txt", "r", encoding="utf-8")
    rw = f.read()
    raw = json.loads(rw)
    f.close()
    for key in raw:
        for idialect in raw[key]:
            name = key+"@"+idialect['informant']
            table = ",sailing,drifting,floating,swimming\n"
            verbs = [] #возможно, сначала придется узнать, что за глаголы у нас есть
            for key2 in idialect:
                if ";" in idialect[key2]:
                    arr = idialect[key2].split(";")
                    for word in arr:
                        if not word in verbs:
                            verbs.append(word)
                else:
                    if not key2 == "informant" and idialect[key2] not in verbs:
                        verbs.append(idialect[key2])
            for verb in verbs:
                xs = ["","","",""]
                for key2 in idialect:
                    for i,el in enumerate(["sailing","drifting","floating","swimming"]):
                        if verb in idialect[el].split(";"):
                            xs[i] = "X"
                str = verb + "," + ",".join(xs)
                table+=str+"\n"
            # print(table)
            write_to_file(name,table)



def data_transform(raw_dct):
    #сначала проверим, нет ли пустых полей
    ver = True
    for key in raw_dct:
        if raw_dct[key] == "":
            ver=False
    if ver:
        f = open("out.txt","r+",encoding="utf-8")
        str_raw = f.read()
        if not str_raw == "":
            dct = json.loads(str_raw)
        else:
            dct = {}
        #нужно сначала выгрузить уже существующие данные в наш словарь dct, а потом уже добавлять новые значения.
        print(raw_dct["lg"]+"=key")
        # print(dct[raw_dct["lg"]])
        if not raw_dct["lg"] in dct:
            dct[raw_dct["lg"]] = [{"informant":raw_dct["informant"],"sailing":raw_dct["sailing"],"drifting":raw_dct["drifting"],
                                   "floating":raw_dct["floating"],"swimming":raw_dct["swimming"]}]
        else:
            dct[raw_dct["lg"]].append({"informant":raw_dct["informant"],"sailing":raw_dct["sailing"],
                                       "drifting":raw_dct["drifting"],"floating":raw_dct["floating"],"swimming":raw_dct["swimming"]})
        f.seek(0,0)
        f.truncate()
        f.write(json.dumps(dct))
        f.close()



@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/input")
def get_input():
    frames = request.args
    print(frames["sailing"])
    data_transform(frames)
    format_data()
    get_table()
    return render_template("redirect.html")

@app.route("/stats")
def get_stats():
    #<img src="{{url_for('static', filename='image_name.jpg')}}" />
    #images = [i for i in os.listdir("images") if i[-4:] == ".png"]
    images = []
    for file in os.listdir("static"):
        if file[-4:] == ".png":
            images.append(("Язык: {}. Информант: {}.".format(file.split("@")[0],file.split("@")[1][:-7]),file))
    print(images)
    return render_template("stats.html",content=images)

@app.route("/results")
def found():
    lg = request.args["lg"].lower()
    lgs = [file.split("@") for file in os.listdir("static") if file[-4:] == ".png"]
    match = []
    fin = []
    ver = False
    for lang in lgs:
        if lg == lang[0].lower():
            match.append(lang)
            ver = True
    for arr in match:
        fin.append(("Язык: {}. Информант: {}.".format(arr[0],arr[1][:-7]),arr[0]+"@"+arr[1]))
        print(fin)
    if ver:
        return render_template("results.html",content=fin)
    else:
        return render_template("not-found.html")



@app.route("/search")
def srch():
    return render_template("search.html")

@app.route("/json")
def raw():
    f = open("out.txt","r",encoding="utf-8")
    content = f.read()
    f.close()
    return render_template("jsn.html",content=content)


if __name__ == "__main__":
    app.run(debug=True)