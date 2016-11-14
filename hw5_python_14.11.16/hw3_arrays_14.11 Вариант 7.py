


def npt():
    ar = []
    for i in range(8):
        ar.append(input("Enter a string: "))
    return ar

def main():
    ar = npt()
    for i in range(0,7,2):
        print(ar[i]+ar[i+1])


main()
