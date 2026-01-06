# Solve the Water jug problem using the Depth First Search technique.
jugs = [0,0]
capacity = list(map(int, input("Enter the capacity for Jug 1 and Jug 2 (separated by space): ").split()))
jug = int(input("Enter the jug number to be filled (1 or 2): ")) - 1
goal = int(input(f"Enter the goal amount in Jug {jug}: "))
stack = []
visited = []
found = False
def put_state(new_state):
    if new_state not in visited:
            stack.append(new_state)
            visited.append(new_state)
def is_goal(current):
    return current[jug] == goal
stack.append(jugs)
visited.append(jugs)
while stack:
    current = stack.pop()
    if is_goal(current):
        found = True
        print("Goal reached:", current)
        break
    if current[0] < capacity[0]:
        new_state = [capacity[0], current[1]]
        put_state(new_state)
    if current[1] < capacity[1]:
        new_state = [current[0], capacity[1]]
        put_state(new_state)
    if current[0] > 0:
        new_state = [0, current[1]]
        put_state(new_state)
    if current[1] > 0:
        new_state = [current[0], 0]
        put_state(new_state)
    if current[0]+current[1] >= capacity[0] and current[1] > 0:
        new_state = [capacity[0], current[1]-(capacity[0]-current[0])]
        put_state(new_state)
    if current[0]+current[1] >= capacity[1] and current[0] > 0:
        new_state = [current[0]-(capacity[1]-current[1]), capacity[1]]
        put_state(new_state)
    if current[0]+current[1] <= capacity[0] and current[1] > 0:
        new_state = [current[0]+current[1], 0]
        put_state(new_state)
    if current[0]+current[1] <= capacity[1] and current[0] > 0:
        new_state = [0, current[0]+current[1]]
        put_state(new_state)
print("Visited States:")
print(visited)
if not found:
    print("Goal not reachable")