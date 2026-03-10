initial = []
goal = []
def heuristic(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if(state[i][j]!=goal[i][j] and state[i][j]!=-1):
                count+=1
    return count
def puzzle(initial,Goal):
    ns = [-1, 0, 1, 0]
    ew = [0, -1, 0, 1]
    visited = []
    queue = []
    found = False
    h = heuristic(initial)
    g = 0
    f = h+g
    queue.append([initial,f])
    while(len(queue)>0):
        i = min(queue,key=lambda x:x[1])
        item = i[0]
        for i in range(3):
            for j in range(3):
                print(item[i][j],end=" ")
            print()
        print("----------")
        queue.remove(i)
        visited.append(item)
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
                    if temp not in visited and temp not in [q[0] for q in queue]:
                        h = heuristic(temp)
                        g = 1
                        f = h+g
                        queue.append([temp,f])
    print("Number of States Visited:",len(visited))
    if(found==False):
        print("Goal State Not Reached")
print("Enter the initial state :")
for i in range(3):
    initial.append(list(map(int,input().split())))
print("Enter the goal state :")
for i in range(3):
    goal.append(list(map(int,input().split())))
print()
puzzle(initial,goal)