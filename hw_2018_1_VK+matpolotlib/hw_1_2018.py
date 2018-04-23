import urllib.request
import json
import matplotlib.pyplot as plt
from dateutil import parser
import datetime
from datetime import date


#https://vk.com/meduzaproject

def get_posts():
    ofsts = [0,100] #скачиваю 200 постов for the sake of simplicity #исправить на 20
    posts = []
    for off in ofsts:
        rqst = urllib.request.Request("https://api.vk.com/method/wall.get?domain=meduzaproject&offset={}"
                                      "&count={}&filter=all&v=5.74&access_token="
                                      "960fe9cb960fe9cb960fe9cbdd966dac859960f960fe9cbccc780c0d7a08fa7ca519279".format(off,"100"))
        rw = {}
        with urllib.request.urlopen(rqst) as fl:
            rw = json.loads(fl.read().decode("utf-8"))
        posts += rw["response"]["items"]
    # print(posts)
    return posts

def get_comments(post_id): #комментарии для одного поста
    ofsts = [0,100] # тоже 200 комментариев (если они есть)
    comments = []
    for off in ofsts:
        rqst = urllib.request.Request("https://api.vk.com/method/wall.getComments?owner_id=-76982440&post_id={}&offset={}&count={}&v=5.74&access_token="
                                      "960fe9cb960fe9cb960fe9cbdd966dac859960f960fe9cbccc780c0d7a08fa7ca519279".format(str(post_id),off,"100"))
        rw = {}
        with urllib.request.urlopen(rqst) as fl:
            rw = json.loads(fl.read().decode("utf-8"))
        # print(rw["response"]["items"])
        comments += rw["response"]["items"]
    # print(comments)
    return comments

def text_out(posts): #эта функция выводит посты и комментарии к ним в .txt файл
    # posts = get_posts()
    posts_text = ""
    for post in posts:
        comments = [comment["text"] for comment in get_comments(post["id"])]
        posts_text +=  "{}\nКомментарии к посту:\n{}\n=============\n".format(post["text"],"\n".join(comments))
    with open("posts.txt","w",encoding="utf-8") as f:
        f.write(posts_text)
    print("end of work")



def count_length(text):
    symbs = ",.?!\'\"()[]+-=^%$#@"
    clean = [w for w in [word.strip(symbs) for word in text.split()] if len(w) > 0] #чистим от лишних символов -- если образовались "слова" с нулевой длиной, их удаляем
    return len(clean)

def comments_len(post): #вычисляет среднюю длину комментария к посту
    lst = [count_length(comment["text"]) for comment in get_comments(post["id"])]
    return sum(lst)/float(len(lst)) if len(lst) > 0 else 0

def get_aver(dct): # на вход структура типа {key:[value1,value2 ... ]} на выходе обычный словарь
    dct_av = {key:sum(dct[key])/float(len(dct[key])) for key in dct}

def length_stats(posts): # в этой функции я решил вручную "нормализовать" график
    pslen = [[count_length(post["text"]),comments_len(post)] for post in posts] # структура: [[длина поста, средняя длина комментария], ...]
    print(pslen)
    post_lens = [10,20,30,40,50,60,70,80,90,100] #for graph (X axis)
    post_lens_dict = {key:[] for key in post_lens}
    comlen = []
    for indx, v in enumerate(post_lens):
        for vlue in pslen:
            if indx != 0:
                if vlue[0] <= v and vlue[0] >= post_lens[indx-1]:
                    post_lens_dict[v].append(vlue[1])
            else:
                if vlue[0] <= v:
                    post_lens_dict[v].append(vlue[1])
    dct_av = {key: sum(post_lens_dict[key]) / float(len(post_lens_dict[key])) for key in post_lens_dict if len(post_lens_dict[key])>0 }
    print(dct_av)
    X = ["0-10"] + [str(post_lens[ind])+"-"+str(v) for ind, v in enumerate(post_lens[1:])]
    print(X)
    # print([dct_av[key] for key in post_lens if key in dct_av])
    # print([dct_av[key] if key in dct_av else 0 for key in post_lens])
    plt.plot(post_lens,[dct_av[key] if key in dct_av else 0 for key in post_lens])
    plt.title("Зависимость длины комментария от длины поста")
    plt.xlabel("Длина поста (слов)")
    plt.ylabel("Средняя длина комментария (слов)")
    plt.xticks(post_lens,X)
    plt.savefig('lenght_of_posts_and_of_comments.png')
    plt.show()

def get_user_age(id):
    try:
        rqst = urllib.request.Request("https://api.vk.com/method/users.get?v=5.74&access_token="
                                      "960fe9cb960fe9cb960fe9cbdd966dac859960f960fe9cbccc780c0d7a08fa7ca519279&fields=bdate&user_ids={}".format(id))
        rw = {}
        with urllib.request.urlopen(rqst) as fl:
            rw = json.loads(fl.read().decode("utf-8"))
        # print(rw)
        braw = [int(el) for el in rw["response"][0]["bdate"].split(".")]
        birth = datetime.date(year = braw[2], month = braw[1],day=braw[0])
        today = date.today()
        return today.year - birth.year - ((today.month,today.day) < (birth.month,birth.day))
    except:
        return 0


def get_user_city(id):
    try:
        rqst = urllib.request.Request("https://api.vk.com/method/users.get?v=5.74&access_token="
                                          "960fe9cb960fe9cb960fe9cbdd966dac859960f960fe9cbccc780c0d7a08fa7ca519279&fields=city&user_ids={}".format(id))
        rw = {}
        with urllib.request.urlopen(rqst) as fl:
            rw = json.loads(fl.read().decode("utf-8"))
        # print(rw)
        return rw["response"][0]["city"]["title"]
    except:
        return ""

def average_for_ages(posts):
    ages = {} #структура: {age:[value1, value 2], age: [] ... }
    for post in posts:
        for comment in get_comments(post["id"]):
            val = get_user_age(comment["from_id"])
            if val != 0:
                if not val in ages:
                    ages[val] = [count_length(comment["text"])]
                else:
                    ages[val].append(count_length(comment["text"]))
    return ages

def average_for_cities(posts):
    cities = {}
    for post in posts:
        for comment in get_comments(post["id"]):
            val = get_user_city(comment["from_id"])
            if val != 0:
                if not val in cities:
                    cities[val] = [count_length(comment["text"])]
                else:
                    cities[val].append(count_length(comment["text"]))
    return cities

def graph_user_ages(posts):
    ages = average_for_ages(posts)
    dct_av = {key: sum(ages[key]) / float(len(ages[key])) for key in ages if len(ages[key]) > 0} #с посчитанными средними значениями
    plt.plot(sorted(dct_av),[dct_av[key] for key in sorted(dct_av)])
    plt.title("Зависимость длины комментария от возраста автора")
    plt.xlabel("Возраст, лет")
    plt.ylabel("Средняя длина комментария (слов)")
    plt.savefig('lenght_of_comments_depending_on_age.png')
    plt.show()

def graph_user_cities(posts):
    cities = average_for_cities(posts)
    dct_av = {key: sum(cities[key]) / float(len(cities[key])) for key in cities if len(cities[key]) > 5}  # с посчитанными средними значениями; отсекаем значения меньше 5, потому что иначе слишком много городов
    Y = [dct_av[city] for city in dct_av]
    X = [city for city in dct_av]
    plt.plot(range(len(X)),Y)
    plt.title("Зависимость длины комментария от города, где живет автор")
    plt.xlabel("Город")
    plt.ylabel("Средняя длина комментария (слов)")
    plt.xticks(range(len(X)),X,rotation=90)
    plt.savefig('lenght_of_comments_depending_on_city.png')
    plt.show()

# print(average_for_ages(get_posts()))
# graph_user_ages()

def main():
    # по умолчанию установлено, что программа скачивает 200 постов и до 200 комментариев к посту.
    # это занимает очень много времени, поэтому, чтобы ее протестировать, можно выше ввести меньшие значения (напр., 5 -- все равно будет небыстро)
    posts = get_posts()
    text_out(posts)
    print("С текстами закончили")
    length_stats(posts)
    graph_user_ages(posts)
    graph_user_cities(posts)

if __name__ == "__main__":
    main()

# for post in get_posts():
#     for comment in get_comments(post["id"]):
#         print(get_user_city(comment["from_id"]))




# count_length("Путин и компания ВОРОВ И ЖУЛИКОВ не оставили нам выбора, кроме как выходить на улицы, поэтому 5 мая.  ) ) ) ")

# length_stats(get_posts())

# text_out()
# get_posts()
# get_comments("1901096")

# 'owner_id': -76982440
# 'id': 1901096
# 'from_id': -76982440













