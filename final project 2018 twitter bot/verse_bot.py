import tweepy
from credentials import *
import markovify
import random
import json
import re
from pymorphy2 import MorphAnalyzer
import string

morph = MorphAnalyzer()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

array = []
with open("starter_data.txt","r+",encoding="utf-8") as f:
    array.append(f.read())
# ran = "пивка! домой! думаю! размышляю! вот подумал я... что не так-то все просто. Так, да. водочки бы -- медвежий угол которая".split(" ")


class war_listener(tweepy.StreamListener):
    def make_sentence(self,arr):
        st = " ".join(arr)
        model = markovify.Text(st, state_size=1)
        sent = ""
        while True:
            gn = model.make_short_sentence(60)
            if not gn:
                continue
            if len(gn) >= 25:
                exclude = ",.?!*%@:;\"\'()[]+=^~`"
                sent = ''.join(ch for ch in gn if ch not in exclude).lower()
                break
        return sent

    def replace_word(self, word):
        fls = ["fet_mirror","pushkin_mirror","krivulin_mirror"]
        dct = {}
        with open(random.choice(fls)+".txt","r",encoding="utf-8") as f:
            dct = json.loads(f.read())
        try:
            features = str(morph.parse(word)[0].tag).split()
            if features[0] in ["PREP", "PRCL"]:
                return word  # предлоги и частицы не заменяются -- потому что pymorphy не учитывает управление предлогов и модальность, которую вносят частицы
            # print(features)
            if features[0] in dct:
                if len(features) == 2:
                    wfin = morph.parse(random.choice(dct[features[0]]))[0].inflect({tg for tg in features[1].split(",")}).word
                else:
                    wfin = random.choice(dct[features[0]])  # в случае, если это, например, предлог, у и него нет непостоянных признаков

                if word[0].isupper():
                    wfin = wfin[0].upper() + wfin[1:]
                # print(wfin)
                return wfin
            else:
                return word
        except:
            print("no")
            return word

    def generator(self, arr):
        sent = self.make_sentence(arr)
        sent3 = ""
        len3 = 0
        len3b = random.choice(range(1,5))
        sent2 = " ".join([self.replace_word(w) for w in sent.split()])
        last_tweet = [(word,morph.parse(word)[0]) for word in arr[len(arr)-1].split()]
        cathegory = random.choice(['NOUN','VERB',"ADVB"])
        for word in last_tweet:
            if cathegory in word[1].tag:
                if len3 < len3b:
                    if cathegory == "NOUN":
                        sent3 += word[1].inflect({'nomn'}).word + " "
                        len3 += 1
                    elif cathegory == "VERB":
                        sent3 += word[1].normalized.word + " "
                        len3 += 1
                    else:
                        sent3 += word[0] + " "
                        len3 += 1
        if len3 < len3b:
            sent3 += "— "*(len3b-len3)
        stroph = random.choice([1,2,3,4,0]) # какой строкой идет отзеркаленная: первой, второй или ее нет вовсе
        if stroph == 1:
            fin = sent + "\n"*random.choice(range(1,3)) + sent2 + "\n"*random.choice(range(2,4)) + sent3
        elif stroph == 2:
            fin = sent2 + "\n"*random.choice(range(1,3)) + sent + "\n"*random.choice(range(2,4)) + sent3
        elif stroph in [3,4]:
            fin = sent + "\n" * random.choice(range(1, 3)) + self.make_sentence(arr) + "\n" * random.choice(range(2, 4)) + sent3
        else:
            fin = sent + "\n"*random.choice(range(1,3)) + sent + "\n"*random.choice(range(2,4)) + sent3
        return fin

    def on_status(self, status):
        if status.user.screen_name != "PoemsWar":
            numb_tweet = 0 # отслеживает, сколько твитов добавляется в алоритм
            delay_const = 20 # каждые сколько твитов генерируется стихотворение
            txt = ""
            try:
                txt = status.extended_tweet['full_text']
            except:
                txt = status.text
            print('Reply to user @{}, tweet: {}'.format(status.user.screen_name, txt))
            # api.update_status(random.choice(ran))
            length = len(array)
            if not re.search("(RT)|(Reply)",txt):
                array.append(txt)
                numb_tweet += 1
                print(length)
            # print(array)
            print("=={}==".format(length))
            if length%delay_const == 0:
                length += 1
                print("\n===============\nBINGO!!!\n================")
                # print(self.generator(array))
                numb_tweet = 0
                api.update_status('{}'.format(self.generator(array)))
                # постим рандомную фразу в ответ
    def on_error(self, status_code):
        if status_code == 420:
            # если окажется, что мы посылаем слишком много запросов, то отсоединяемся
            return False
        # если какая-то другая ошибка, постараемся слушать поток дальше
        return True

war_listener = war_listener()
myStream = tweepy.Stream(auth = api.auth, listener=war_listener)
myStream.filter(track=['война','войну','войны','войне','войной'])

