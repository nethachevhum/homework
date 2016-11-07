a = int(input("enter number"))
b = 2
q = 2

if a < 2:
    print("no way")

else:
    while True:
        if b <= a:
            print(b)
        else:
            break
        b = 2**q
        q += 1
