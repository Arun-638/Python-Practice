L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
counte = 0
counto = 0
for i in L:
    if i%2 == 0:
        counte+=1
    else:
        counto+=1
print("The count of even and odd elements in the list are ",counte,counto)