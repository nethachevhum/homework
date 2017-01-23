import random


##идея такая: программа работает как с теми биграммами, в которых угадывается первый елемент, так и с теми,
##в которых угадывается второй. 
def open_file():
    f = open("d.csv","r") #три колонки: в первой указывается порядок слов
    ar = []
    for line in f.readlines():
        ar.append(line.split())
    f.close()
    return ar

def create_d(ar):
    d = {}
    for line in ar:
        if line[0] == "inv":
            d[line[2]] = line[1] + "*" #ставим звездочку тогда, когда в словарь биграмм записывается не в прямом порядке
        elif line[0] == "n":
            d[line[1]] = line[2]
    return d

        
def verify(word):
    inp = input("Угадайте слово: ")
    if inp == word:
        print(congr(True))
    else:
        print(congr(False))

def congr(sw):
    pos = ["Вы угадали!","Ура, Вы угадали!","Угадали...","Наконец-то! Вы угадали!","Неужели вы -- угадали?.."]
    neg = ["Не угадали, попробуйте еще.","Неправильно.","Увы -- неправильно...","Вовсе нет, пробуйте еще."]
    if sw:
        return random.choice(pos)
    else:
        return random.choice(neg)

def guess(d):
    key = random.choice(list(d.keys()))
    ar = [key,d[key]]
    if ar[1].endswith("*"):
        print(ar[1].strip("*") + "...")
        verify(ar[0])
    else:
        print("..." + ar[1])
        verify(ar[0])
        

def main():
    while True:
        guess(create_d(open_file()))
        if input("Хотите продолжить? Сделайте пустой ввод, если хотите. Если нет -- введите что-нибудь: ") != "":
            print("До свидания!")
            break
        


if __name__ == "__main__":
    main()







