

##Я подумал, что неплохо сделать проверку -- на случай, если пользователь введет на только цифры. И убрал это в функцию. Насколько это рационально?
def intver():
    a = input("Enter the number:")
    while not a.isdigit():
        a = input("You shouldn't enter any letters. Enter again:")

    a = int(a)
    return a

a = intver()
b = intver()
c = intver()

if a/b == c:
    print("a/b=c")
else:
    print("a/b doesn't equal c")

if a**b == c:
    print("a^b=c")
else:
    print("a^b doesn't equal c")




