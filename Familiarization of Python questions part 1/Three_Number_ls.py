a = int(input("Enter the First Number: "))
b = int(input("Enter the Second Number: "))
c = int(input("Enter the Third Number: "))
largest = a
smallest = a
if b>largest:
    largest = b
if b<smallest:
    smallest = b
if c>largest:
    largest = c
if c<smallest:
    smallest = c
print("The largest Number is : ",largest)
print("The smallest Number is : ",smallest)