##для каждого задания своя функция

def task1():
    f = open('freq.txt','r',encoding = "UTF-8")
    line = []
    for i in f:
        line = i.split(' | ')
        if line[1] == 'союз':
            print(' | '.join(line))
    f.close()

def task2():
    f = open('freq.txt','r',encoding = "UTF-8")
    line = []
    nom = []
    st = ""
    summ = 0
    for i in f:
        line = i.split(' | ')
        nom = line[1].split()
        if nom[0] == "сущ" and len(nom)==5: ##видимо, у каких-то существительных меньше пяти признаков -- ошибка программы? Их мы не считаем.
            if nom[2] == "ед" and nom[3] == "жен":
                st += line[0] + ", "
                summ += float(line[2])
        
    f.close()
    print(st)
    print("Суммарный ipm: ", summ)
        
        
def npt():
    #функция ввода для третьего задания
    ary = []
    while True:
        np = input("Enter a word").lower()
        if np == "":
            print("Конец ввода")
            break
        ary.append(np)
    return ary


def task3():
    ary = npt()
    f = open('freq.txt','r',encoding = "UTF-8")
    line = []
    dictio = []
    ver = False
    for i in f:
        dictio.append(i.split(" | "))
    for word in ary:
        for i in range(len(dictio)):
            ver = False
            if word == dictio[i][0]:
                print("Для слова " + "\"" + word + "\"" + ": "+ dictio[i][1]+ " | "+ dictio[i][2])
                ver = True
                break
        if not ver:
            print("Слова " + "\""+ word +"\" " + "в словаре нет.")
            

    f.close()
    
        
            
##сделал общую функцию для проверки. Можно тестировать каждое задание много раз, если ввести что-то, кроме номера, программа закроется.
def main():
    while True:
        a = int(input("Введите номер задания: "))
        if a == 1:
            task1()
        elif a==2:
            task2()
        elif a==3:
            task3()
        else:
            break

if __name__ == '__main__':
    main()















