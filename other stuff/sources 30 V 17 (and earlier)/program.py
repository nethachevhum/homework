#1) добавить  строку с features (т.е. продублировать для всех языков)
#2) перевести все в строки (хотя это должна быть первая)
#3)* вообще, можно сделать так, что мне выдается сразу строка в r, чтобы не вбивать все вручную

#убрать первую строку в csv



##NB!!! У этой программы есть недостаток -- кавычки при обозначениии координат не нужны

def getar(inp):
    f = open(inp + ".csv",'r',encoding="utf-8") #название файла без .csv!
    a = f.read().split("\n")
    b = []
    for el in a:
        b.append(el.split(";"))
    return b

def add_feature(arX,arY):
    ar1 = arX
    ar2 = arY
    ar = []
    arr = []
    #проще сделать новый массив, куда пихать все совпадения (иначе с enumerate)
    for line2 in ar2:
        for line1 in ar1:
            if line2[0] == line1[1]:
                ar.append("*".join(line1)+"*"+line2[1])
    for line in ar:
        arr.append(line.split("*"))

    for i in range(0,100):
        print(arr[i])
    return arr



def getlines(ar):
    lines = []
    lines1 = []
    for i in range(0,len(ar[1])):
        lines.append("")

    for n in range(0,len(ar[1])):
        for line in ar:
            if not n in [4,5]:
                lines[n] += "\"{}\", ".format(line[n])
            elif n in [4,5]:
                lines[n] += "{}, ".format(line[n])

    for line in lines:
        lines1.append(line[:-2])

    return lines1
            




          
def outp(ar):
##     f = open("output.txt",'w+',encoding="utf-8")
##     f.write(text)
    # сверху простой аутпут -- нужен при ручном копировании
    f = open("output.txt",'w+',encoding="utf-8")
    st = "locat <- data.frame(language = c({}), dialect = c({}), latitude = c({}), longitude = c({}), feature = c({}))".format(ar[1],ar[2],ar[3],ar[4],ar[5])
    f.write(st)
    
    
    
outp(getlines(add_feature(getar("csv-template"),getar("features"))))




##map.feature(circassian$language,
##            features = circassian$dialect,
##            stroke.features = circassian$language,
##            latitude = circassian$latitude,
##            longitude = circassian$longitude)


##df$popup <- c ("sɐ s-ɐ-k'ʷɐ<br> 1sg 1sg.abs-dyn-go<br>'I go'",
##               "sɐ s-o-k'ʷɐ<br> 1sg 1sg.abs-dyn-go<br>'I go'",
##               "id-ę<br> go-1sg.npst<br> 'I go'",
##               "ya id-u<br> 1sg go-1sg.npst <br> 'I go'",
##               "id-a<br> go-1sg.prs<br> 'I go'")

##"df <- data.frame(language = c({1}), dialect = c({2}), latitude = c({3}), longitude = c({4}), feature = c({5}))"



          
##def joining(ar):
##    arr = []
##    for line in ar:
##        arr.append(line.split("*"))
##    for i in range(0,100):
##        print(arr[i])



#outp(add_feature(getar("csv-template"),getar("features")))


##ar = add_feature(getar("csv-template"),getar("features"))
##for i in range (1,10):
##    print(ar[i])

##for n in range(0,10):
##    print(getar("csv-template")[n][1])
#getar()
