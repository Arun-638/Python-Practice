# The hacker encounters a staircase-like encryption system.

# To escape, he can climb 1 or 2 steps at a time.

# Given an integer n, find the total number of distinct ways to reach the top.
# Input Format

# Integer n
# Constraints

# 1 ≤ n ≤ 45
def escape(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
n = int(input())
print(escape(n))
