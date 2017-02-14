#все пункты по разным функциям
import re


def getar():
    f = open("download-excel.xml","r",encoding = "utf8")
    ar = f.read()
    f.close()
    return ar


def count_lines(ar): #п.1: подсчет строк
    f = open("out1.txt","w",encoding="utf8")
    f.write(str(len(ar.split("\n")))) #в конце корпуса -- пустая строка, она тоже считается
    f.close()

def dct_morph(ar):
    arr = re.findall("<w lemma=\"(?:.*?)\" type=\"(.*?)\">(?:.*?)</w>",ar)
    dct = {}
    for key in arr:
        if key not in dct:
            dct[key] = 1
        else:
            dct[key] += 1
    return dct

def dct_morph_out(dct): #это для второго пункта, вместе с предыдущей функцией. Можно было сделать проще, с open("",a), но были бы риски
    f = open("out2.txt","w",encoding="utf8")
    st = ""
    for key in dct:
        st = st + str(key) + "\n" 
    f.write(st)
    f.close()

def find_adj(text):
    arr = re.findall("<w lemma=\"(?:.*?)\" type=\"(l.f.*?)\">(?:.*?)</w>",text)
    dct = {}
    for key in arr:
        if key not in dct:
            dct[key] = 1
        else:
            dct[key] += 1
    return dct


def find_adj_out(dct):
    f = open("out3.txt","w",encoding="utf8")
    st = ""
    for key in dct:
        st = st + str(key) + " " + str(dct[key]) + "\n" 
    f.write(st)
    f.close()


def look_better(text):
    arr = re.findall("<w lemma=\"(.*?)\" type=\"(l.f.*?)\">(.*?)</w>",text)
    st = ""
    for el in arr:
        st = st + el[0] + "," + el[1] + "," + el[2] + "\n" 
    text1 = re.sub("<body>(.|\n)*</body>","<body>\n"+st+"\n</body>",text)
    f = open("out4.csv","w",encoding="utf8")
    f.write(text1)
    f.close()

def main():
    while True:
        st = input('Введите 1 для 1 п., 2 для 2 п., 3 для 3 п. задания, любой другой символ для выхода:')
        if st == "1":
            count_lines(getar())
        elif st == "2":
            dct_morph_out(dct_morph(getar())) 
        elif st == "3":
            find_adj_out(find_adj(getar())) #это первый пункт задания 3 (разборы прилагательных и число вхождений)
            look_better(getar()) #это второй пункт задания 3 (перезапись в .csv)
            #все файлы аутпута создаются сами, в т.ч. для последнего задания, или перезаписываются
        else:
            print("До свидания.")
            break

if __name__ == "__main__":
    main()
#look_better(getar())
#find_adj_out(find_adj(getar()))

#dct_morph_out(dct_morph(getar()))

#print(dct_morph(getar()))
#count_lines(getar())
#print("\n".join(getar()))
