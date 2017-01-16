

def getwords():
    f = open("hemingway.txt",'r')
    ar = f.read().split()
    f.close()
    for i,word in enumerate(ar):
        ar[i] = word.strip("!?.”,:;’\'\"-—“").lower()
    return(ar)

def un(ar):
    arr = []
    for word in ar:
        if word.startswith('un'):
            arr.append(word)
    return(arr)

def verify(ar,inp):
    amount = 0
    for word in ar:
        if len(word)>inp:
            amount += 1
    return str(amount/len(ar)*100)+"%"+" of words are longer than " + str(inp) + " letters."
    
def main():
    while True:
        inp = int(input("Enter a number. Enter 0 to close the program. "))
        if inp > 0:
            print(verify(un(getwords()),inp))
        else:
            print("Bye!")
            break

if __name__ == "__main__":
    
    main()
