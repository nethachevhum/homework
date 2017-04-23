import os

def find_folder():
    #здесь можно было бы обойтись без словарь, но если мы хотим учесть случай, когда у нас несколько папок с одинаковым
    #числом файлов, разумнее всего сделать со словарями
    dct = {}
    mco = 0 #наибольшее число файлов в папке: функция возвращает словарь и это число
    for root,dirs,files in os.walk('.'):
        c = 0
        for file in files:
            c+=1
        if c > mco:
            mco = c
        if not c == 0:
            dct[root.split('\\')[len(root.split('\\'))-1]] = c
    return dct, mco

def find_right_one(dct,mco):
    ar = []
    for key in dct:
        if dct[key] == mco:
            ar.append(key)
    return ar

def main():
    ar = find_right_one(find_folder()[0],find_folder()[1])
    print("Папка(-и), где больше всего файлов: " + " | ".join(ar))
    #случая, когда файлов нет нигде, быть не может -- всегда есть сама папка с питоновским файлом



if __name__ == "__main__":
    main()
    
