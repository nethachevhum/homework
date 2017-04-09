import re

def getar_sentences():
    f = open("solj.txt",'r',encoding="utf-8")
    st = f.read()
    ar = [re.sub("\n"," ",re.sub("[,;\"}:-]",'',sentence).lower()) for sentence in re.split('[!?.]', st) if sentence != '']
    f.close()
    return ar

def freq(word,ar):
    count = 0
    for w in ar:
        if w == word:
            count += 1
    return count


    

def count_rep(ar):
    arr = [sentar.split() for sentar in ar]
    for sentence in arr:
        d = {word:freq(word,sentence) for word in sentence}
        for key in d:
            if d[key] > 1:
                print('{}{:^20}'.format(key,d[key]))
    for sentence in arr:
        for word in sentence:
            if not word in d:
                d[word] = 1
            else:
                d[word] += 1
    
def main():
    count_rep(getar_sentences())

if __name__ == "__main__":
    count_rep(getar_sentences())
main()
