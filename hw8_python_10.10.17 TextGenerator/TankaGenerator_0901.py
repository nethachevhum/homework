##Исходное стихотворение:
##Сарумару Таю. (пер. Н.Н.Бахтина, из сб. "Песни ста поэтов" 1905 г.)
##
##‎Как грустно слышать
##осеннею порою
##‎в горах пустынных
##средь зелени увядшей
##протяжный крик оленя!

##Программа генерирует аналогичные по структуре тексты, вариативность небольшая, но тексты должны выходить
##интересней и осмысленней, чем в примере.
##Метрическая структура оригинального текста сохранена.

import random ##и это тоже нужно убрать в фукнцию?

def file_op(name): ##открывает файл и создает массив
    f = open(name,'r')
    ar = f.read().split(' ')
    f.close()
    return(ar)




def adverb(): ##наречия в файле -- двусложные с ударением на первом слоге
    ar = file_op("adverbs.txt")
    return random.choice(ar) + ' '

def int_clit():
    ##здесь клитики для первой строфы, включая междометья
    ar = file_op("int_clitics.txt")
    return random.choice(ar) + ' '

def verb():
    ##здесь должны быть переходные глаголы чувств с ударением на первом слоге
    ar = file_op("verbs.txt")
    return random.choice(ar) + ' '


def name_fem():
    ##существительные ж.р., трехсложные, с ударением на 3 слог, в тв. падеже; семантика времени
    ar = file_op("name_fem.txt")
    return random.choice(ar) + ' '

def adj_fem1():
    ##прилагательные ед.ч жр.р. тв.п., четырехсложные с ударением на втором слоге. Семантически я пытался как-то согласовать с name_fem
    ar = file_op("adj_fem1.txt")
    return random.choice(ar) + ' '
def adj_fem2():
    ##то же, что в предыдущей функции, но с ударением на 3-м слоге
    ar = file_op("adj_fem2.txt")
    return random.choice(ar) + ' '

def prepositions1():
    ##здесь односложные пространственные предлоги, требующие род.п.
    ar = file_op("prepositions1.txt")
    return random.choice(ar) + ' '

##def prepositions0():
##    ##пространственные предлоги, не образующие слога; требующие пр.п. Похоже, здесь только "в", но, может, и еще что-то есть, так чт
##    ar = file_op("prepositions0.txt")


def names_prcaus(q):
    ##существительные в пр.п.: в SG и PL. Существительные в PL берем любого рода, в SG -- только мужского и среднего (для простоты)
    if q == "sg":
        ar = file_op("names_prcaus_sg.txt")
        return random.choice(ar) + ' '
    elif q == "pl":
        ar = file_op("names_prcaus_pl.txt")
        return random.choice(ar) + ' '

def adj_prcaus(q):
    if q == "sg":
        ar = file_op("adj_prcaus_sg.txt")
        return random.choice(ar) + ' '
    elif q == "pl":
        ar = file_op("adj_prcaus_pl.txt")
        return random.choice(ar) + ' '


def name_gen():
    ##существительные ед.ч. ж.р. в генитиве
    ar = file_op("name_gen.txt")
    return random.choice(ar) + ' '

def adj_gen():
    ##существительные ед.ч. ж.р. в генитиве
    ar = file_op("adj_gen.txt")
    return random.choice(ar) + ' '


def name_nom():
    ar = file_op("name_nom.txt")
    return random.choice(ar) + ' '

def adj_nom():
    ar = file_op("adj_nom.txt")
    return random.choice(ar) + ' '

def name_gen_sg():
    ar = file_op("name_gen_sg.txt")
    return random.choice(ar)    

def punct():
    ar = file_op("punct.txt")
    return random.choice(ar)    

def verse1():
    return int_clit() + adverb() + verb()

def verse2(): ##два варианта второй строфы: либо существительное на первом месте, либо прилагательное.
    if random.randint(1,2) == 1: ##для сохранения метра прилагательные выбираются из разных списков
        return(name_fem() + adj_fem2())
    return(adj_fem1() + name_fem())

def verse3():    
    if random.randint(1,2) == 1:
        return "в " + names_prcaus("sg") + adj_prcaus("sg")
    return "в " + names_prcaus("pl") + adj_prcaus("pl")

def verse4():
    return prepositions1() + name_gen() + adj_gen()


def verse5():
    return adj_nom() + name_nom() + name_gen_sg() + punct()

def main():
    print("Ныне забытый поэт-символист В.К. в начале 20 в. написал цикл стихотворений танка; цикл посвящен В.Я. Брюсову. \nВ.К. \nПять танок.")
    for i in range(1,6):
        print(i)
        print(verse1().capitalize() + "\n" + verse2().capitalize() + "\n" + verse3().capitalize() + "\n" + verse4().capitalize() + "\n" + verse5().capitalize())
    print("1908 г.")

main()

##Этот замысел можно было реализовать более рационально; в рамках задания имело смысл сделать что-то более бессмысленное -- похожее на то, что в примере.
##Чтобы вполне реализовать концепт, нужно еще поработать со словарем, пока что он слишком беден.
##Хорошо было бы взять словарь Брюсова и Белого, но на текущем этапе это невозможно, вручную слишком долго.
##Так что слова подбирались интуитивно.


    
