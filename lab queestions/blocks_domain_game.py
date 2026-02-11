def heuristic1(state, goal_state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if j >= len(goal_state[i]) or state[i][j] != goal_state[i][j]:
                count += 1
    return count
def heuristic2(state, goal_state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] not in goal_state[i]:
                count += 1
    return count
def heuristic3(state, goal_state):
    count = 0
    for i in range(len(state)):
        count += abs(len(state[i]) - len(goal_state[i]))
    return count

def get_states(state):
    states = []
    for i in range(len(state)):
        if state[i]: 
            block = state[i][-1]
            for j in range(len(state)):
                if i != j:
                    new_state = [s[:] for s in state]
                    new_state[i].pop()
                    new_state[j].append(block)
                    states.append(new_state)
    return states
def Blocks_domain(initial, goal,heuristic):
    open = []
    closed = []
    open.append((initial, heuristic(initial, goal)))
    while open:
        item = min(open, key=lambda x: x[1])
        open.remove(item)
        state = item[0]
        if state not in closed:
            if state == goal:
                print("State: ",state)
                print("Goal state reached")
                print("Number of Visited States:", len(closed))
                return len(closed)
            closed.append(state)
            for i in get_states(state):
                if i not in closed:
                    h = heuristic(i,goal) 
                    open.append((i, h))
    print("Goal state not reachable.")
initial = []
goal = []
print("Enter the initial state: ")
for i in range(3):
    block = input("Enter the blocks in stack " + str(i+1) + ": ").split()
    initial.append(block)
print("Enter the Goal state: ")
for i in range(3):
    block = input("Enter the blocks in stack " + str(i+1) + ": ").split()
    goal.append(block)
h1 = Blocks_domain(initial, goal,heuristic1)
h2 = Blocks_domain(initial, goal,heuristic2)
h3 = Blocks_domain(initial, goal,heuristic3)
print("Heuristic 1:", h1)
print("Heuristic 2:", h2)
print("Heuristic 3:", h3)
if h1 < h2 and h1 < h3:
    print("Heuristic 1 is the best heuristic for this problem.")
elif h2 < h1 and h2 < h3:
    print("Heuristic 2 is the best heuristic for this problem.")
else:
    print("Heuristic 3 is the best heuristic for this problem.")
# initial = [['E'], ['B', 'F'], ['D', 'A', 'C']]
# goal = [['A', 'D', 'B'], ['E', 'F', 'C'], []]