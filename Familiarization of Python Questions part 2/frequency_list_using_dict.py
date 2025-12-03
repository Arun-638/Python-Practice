L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
d = {}
for i in L:
    if i in d:
        d[i]+=1
    else:
        d[i] = 1
print(d)