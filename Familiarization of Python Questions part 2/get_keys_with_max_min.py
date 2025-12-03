d = {}
n = int(input("Enter the number of key: "))
for _ in range(n):
    k = input("Enter the key: ")
    v = int(input("Enter the value: "))
    d[k] = v
Max = max(d.values())
Min = min(d.values())
for key,value in d.items():
    if value == Max:
        Max = key
    if value == Min:
        Min = key
print("The max and min key of the dictionary are ",Max,"and",Min)