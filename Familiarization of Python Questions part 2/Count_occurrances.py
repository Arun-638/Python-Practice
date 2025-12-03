L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
search = int(input("Enter the element to Find the occurrances : "))
count = 0
for i in L:
    if search == i:
        count+=1
print("The number of occurrences of the given element is ",count)