initial = []
Goal = []
def puzzle(initial,Goal):
    ns = [-1,1,0,0]
    ew = [0,0,-1,1]
    visited = []
    queue = []
    found = False
    queue.append(initial)
    visited.append(initial)
    while(len(queue)>0):
        item = queue.pop(0)
        for i in range(3):
            for j in range(3):
                print(item[i][j],end=" ")
            print()
        print()
        if(item==Goal):
            print("Goal State Reached")
            found = True
            break
        else:
            for i in range(3):
                for j in range(3):
                    if(item[i][j]==-1):
                        x = i
                        y = j
            for i in range(4):
                newx = x+ns[i]
                newy = y+ew[i]
                if(newx>=0 and newx<3 and newy>=0 and newy<3):
                    temp = []
                    for k in item:
                        temp.append(k.copy())
                    temp[x][y],temp[newx][newy] = temp[newx][newy],temp[x][y]
                    if temp not in visited:
                        queue.append(temp)
                        visited.append(temp)
    if(found==False):
        print("Goal State Not Reached")
print("Enter the initial state :")
for i in range(3):
    initial.append(list(map(int,input().split())))
print("Enter the goal state :")
for i in range(3):
    Goal.append(list(map(int,input().split())))
print()
puzzle(initial,Goal)