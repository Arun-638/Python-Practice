def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
n = int(input("Enter the number to find the factorial: "))
result = factorial(n)
print("Factorial of this number is",result)