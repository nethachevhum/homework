import os
import re


def open_file(name):
    f = open(name,"r")
    txt = f.read()
    f.close()
    return re.findall("<w>.*</w>", txt)

def write_to_file(st,filename): #просто записывает строку в новый файл; NB, что filename должен быть с форматом файла
    f = open(filename,"w+",encoding = "utf-8")
    f.write(st)
    f.close()

def count_words_infile(): #первое задание
    st = "" #сюда вписывается число слов в каждом файле
    for roots,dirs,files in os.walk("."):
        for file in files:
            if file.endswith(".xhtml"):
                st = st + file + "\t"+ str(len(open_file(os.path.join(roots,file)))) + "\n"
    write_to_file(st,"output_1.txt")


def find_data():
    fd = [] ##файл-автор-дата создания
    for roots,dirs,files in os.walk("."):
        for file in files:
            if file.endswith(".xhtml"):
                with open(os.path.join(roots,file)) as text:
                    if file.endswith(".xhtml"):
                        t = text.read()
                        fd.append([file,"".join(re.findall("<meta content=\"([а-яА-ЯёЁ ]+)\" name=\"author\"></meta>",t)),\
                                   "".join(re.findall("<meta content=\"(.*)\" name=\"created\"></meta>",t))])
    st = ""
    for line in fd:
        st = st + "\t".join(line) + "\n"
    print(st)
        







find_data()
#count_words_infile() 


#find_data()
#print("\n".join(open_file("_itartass1")))
