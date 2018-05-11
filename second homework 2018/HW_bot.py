# -*- coding: utf-8 -*-
from pymorphy2 import MorphAnalyzer
import json
import os.path
import random
import re
import flask
import telebot
import conf

morph = MorphAnalyzer()


# программа работает так: сначала она смотрит на частотный словарь из НКРЯ, и делает словарь {}, где
# ключи -- постоянные признаки слова, а значения -- подходящие слова.
# после парсится введенная пользователем фраза -- для каждого слова в словаре ищутся слова с теми же
# постоянными признаками. Если таких нет, слово остается тем же.

def create_dict():
    dct = {}
    with open("1grams-3.txt", "r", encoding="utf-8") as f:
        arr = [word for word in f.read().split() if not any(char.isdigit() for char in word)]
        # print(arr)
        for word in arr:
            # print(dct)
            inherent = str(morph.parse(word)[0].tag).split()[0]
            if not inherent in dct:
                dct[inherent] = [word.lower()]
            else:
                if not word in dct[inherent]:
                    dct[inherent].append(word.lower())
    # print(dct)
    return dct

def get_dct(): #размеченный словарь лежит в текстовом файле в формате .json. если ничего не нашлось -- разметка происходит заново.
    if os.path.isfile("work_dict.txt"):
        with open("work_dict.txt", "r+", encoding="utf-8") as f:
            return json.loads(f.read())
    else:
        with open("work_dict.txt","w+",encoding="utf-8") as f:
            dc = json.dumps(create_dict(), ensure_ascii=False)
            f.write(dc)
            return dc


def replace_word(word):
    dct = get_dct()
    try:
        features = str(morph.parse(word)[0].tag).split()
        if features[0] in ["PREP","PRCL"]:
            return word #предлоги и частицы не заменяются -- потому что pymorphy не учитывает управление предлогов и модальность, которую вносят частицы

        # print(features)
        if features[0] in dct:
            if len(features) == 2:
                wfin = morph.parse(random.choice(dct[features[0]]))[0].inflect({tg for tg in features[1].split(",")}).word
            else:
                wfin = random.choice(dct[features[0]]) #в случае, если это, например, предлог, у и него нет непостоянных признаков

            if word[0].isupper():
                wfin = wfin[0].upper() + wfin[1:]
            # print(wfin)
            return wfin
        else:
            return word
    except:
        return word
# def cleanse(text):
#     symbs = ",.?!\'\"()[]+-=^%$#@"
#     clean = [w for w in [word.strip(symbs) for word in text.split()] if len(w) > 0] #чистим от лишних символов -- если образовались "слова" с нулевой длиной, их удаляем
#     return clean
#

def replace_sentence(sent):
    symbs = ",.?!\'\"()[]+-=^%$#@"
    arr = [re.sub(r"(?:[а-яА-ЯёЁ]+)([,.?!\'\"()[\]+-=^%$#@]*)",r"{}\1".format(replace_word(word.strip(symbs))),word) for word in sent.split()]
    return " ".join(arr)
print(replace_sentence("Сначала я был на Рижской. Там купил себе пивка, но оно было безалкогольное. Не считается..."))

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot = telebot.TeleBot(conf.TOKEN,threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
app = flask.Flask(__name__)

@bot.message_handler(func=lambda m: True)
def replace_sent(message):
    bot.send_message(message.chat.id,"Дружище, правильно ли я понял, что ты имел в виду это \"{}\"?".format(replace_sentence(message.text)))

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "ok"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json   ':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)






            # /home/leshathegoat/.virtualenvs/myvirtualenv/bin/python


# replace_word("делая")

# print(get_dct())



# print(morph.parse("щас")[0].tag)
# w2 = morph.parse("стужа")[0]
# print(w1)
# print(w2.inflect({tg for tg in str(w1).split(",")}))





# a = "accs,sing"
# print(morph.parse("лодка")[0].inflect({tg for tg in a.split(",")}))

# print(b.inflect(get_analysys("стаканчик")))
# print(b.inflect({'sing'}))
#print(b.inflect(get_analysys("пидор")))