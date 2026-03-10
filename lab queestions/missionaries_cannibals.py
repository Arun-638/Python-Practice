def isgoal(state, M, C):
    m, c, d = state
    if m < 0 or c < 0 or m > M or c > C:
        return False
    if m > 0 and m < c:
        return False
    mr = M - m
    cr = C - c
    if mr > 0 and mr < cr:
        return False
    return True

def heuristic(state):
    m, c, d = state
    return m + c

def getstate(state, M, C):
    m, c, boat = state
    moves = [(1,0),(2,0),(0,1),(0,2),(1,1)]
    states = []

    for i, j in moves:
        if boat == 0:
            new_state = (m - i, c - j, 1)
        else:
            new_state = (m + i, c + j, 0)
        if isgoal(new_state, M, C):
            states.append(new_state)

    return states

def missionaries_cannibals(M, C):
    initial = (M, C, 0)
    goal = (0, 0, 1)

    visited = []
    queue = []

    g = 0
    h = heuristic(initial)
    f = g + h
    queue.append((initial, g, f, [initial]))

    while queue:
        node = min(queue, key=lambda x: x[2])
        queue.remove(node)

        state, g, f, path = node
        visited.append(state)

        if state == goal:
            print("Goal Reached")
            print("Path:")
            for p in path:
                print(p)
            return
        states = getstate(state, M, C)
        for temp in states:
            if temp not in visited:
                new_g = g + 1
                h = heuristic(temp)
                new_f = new_g + h
                queue.append((temp, new_g, new_f, path + [temp]))
    print("Goal Not Reached")
M = int(input("Enter the number of missionaries: "))
C = int(input("Enter the number of cannibals: "))
missionaries_cannibals(M, C)