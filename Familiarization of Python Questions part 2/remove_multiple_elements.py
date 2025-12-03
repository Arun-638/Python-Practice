L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
L = list(set(L))
for i in L:
    print(i,end = " ")