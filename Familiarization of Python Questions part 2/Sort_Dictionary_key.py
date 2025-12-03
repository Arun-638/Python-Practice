d = {}
n = int(input("Enter the number of key: "))
for _ in range(n):
    k = input("Enter the key: ")
    v = int(input("Enter the value: "))
    d[k] = v
d = {key : d[key] for key in sorted(d.keys())}
print(d)