import os

def cyr_lat(cyr,lat,st):
    iscyr = False
    islat = False
    for letter in st:
        if not iscyr and letter in cyr:
            iscyr = True
        elif not islat and letter in lat:
            islat = True
        if iscyr and islat:
            return True

def find_folders():
    ar = os.listdir('.')
    c = 0
    for sth in ar:
        if os.path.isdir(sth) and cyr_lat('абвгдеёжзийклмнопрстуфхцчшщъыьэюя','abcdefghijklmnopqrstuvwxyz',sth):
            c += 1
    return c

def nrep_list():
    ar = os.listdir('.')
    dct = {}
    for el in ar:
        if os.path.isdir(el):
            dct[el]=1
        else:
            for i in range(0,len(el)):
                if el[len(el)-1-i] == ".":
                    dct[el[:len(el)-1-i]]=1 #мне как-то не хотелось вручную убирать повторения, поэтому я сделал словарь.
                    break                      #вероятно, есть более элегантное решение (другой тип данных?)
    print('\n'.join([key for key in dct]))

def main():
    print("{} пап(ка|ки|ок) с кириллическими и латинскими символами. \nНеповторяющиеся имена файлов/папок:".format(find_folders()))
    nrep_list()


if __name__ == '__main__':
    main()


    


