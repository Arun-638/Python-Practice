d = {}
n = int(input("Enter the number of key: "))
for _ in range(n):
    k = input("Enter the key: ")
    v = int(input("Enter the value: "))
    d[k] = v
key = input("Enter the key: ")
if key not in d:
    print("Key doesnt exist")
else:
    print("Key Exists")