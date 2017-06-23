import os
import re

#было бы умно вынести это os.walk в отдельную функцию. Но я начал делать без нее, и в итоге на это у меня не хватило времени -- хотя это должно быть быстро.

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
    st = "Название файла;Автор;Год создания\n"
    for line in fd:
        st = st + ";".join(line) + "\n"
    write_to_file(st,"output_2.csv")


def find_bigrams():
    for roots,dirs,files in os.walk("."):
        for file in files:
            if file.endswith(".xhtml"):
                ar = open_file(os.path.join(roots,file))
                for i,word in enumerate(ar): #а здесь можно было обойтись и без enumerate
                    if re.search("<w><ana lex=\"(.+)\" gr=\"A.*gen",word):
                        if re.search("<w><ana lex=\"(.+)\" gr=\"S.*gen",ar[i+1]):
                            print(re.search("ana>(.+)<",word).group(1)+" " +re.search("ana>(.+)<",ar[i+1]).group(1))

                        




find_bigrams()



#find_data()
#count_words_infile() 


#find_data()
#print("\n".join(open_file("_itartass1")))
