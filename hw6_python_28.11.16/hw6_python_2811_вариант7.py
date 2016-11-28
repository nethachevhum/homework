def main():
    st = input("Enter a string: ")
    print(st)
    while len(st) > 1:
        st = st[1:len(st)-1]
        print(st)
    
main()
