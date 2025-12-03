L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
largest = max(L)
smallest = min(L)
print("The smallest and largest in the list are ",smallest,largest)