L = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = int(input("Enter the element: "))
    L.append(element)
Sum = sum(L)
Average = Sum/n
print("The sum and average of the elements are ",Sum,"and",Average)