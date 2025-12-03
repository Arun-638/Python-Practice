n = int(input("Enter the number: "))
first = 0
second = 1
if n == 0:
    print("No series")
elif n == 1:
    print(first,end=" ")
else:
    print(first,second,end=" ")
    for i in range(2,n):
        third = first+second
        print(third,end = " ")
        first,second = second,third