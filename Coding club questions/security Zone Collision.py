# Inside the system, security zones are represented as rectangles.

# You are given two rectangles defined by their bottom-left and top-right coordinates: - (x1, y1, x2, y2) - (x3, y3, x4, y4)

# Determine whether the two rectangles overlap with positive area
def security(rec1,rec2):
    x1, y1, x2, y2 = rec1
    x3, y3, x4, y4 = rec2
    if x1 >= x4 or x3 >= x2:
        return False
    if y1 >= y4 or y3 >= y2:
        return False
    
    return True
rec1 = list(map(int,input().split()))
rec2 = list(map(int,input().split()))
if security(rec1,rec2):
    print("true")
else:
    print("false")