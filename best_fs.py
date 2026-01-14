open = []
closed = []
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5), ('C', 1)],
    'C': [('D', 1)],
    'D': []
}
heuristic = {
    'A': 4,
    'B': 2,
    'C': 1,
    'D': 0
}
def backtrack_path(closed,goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        for node, parent in closed:
            if node == current:
                current = parent
                break
    path.reverse()
    return path
def best_first_search(graph, start, goal, heuristic):
    open.append((start, heuristic[start]))
    closed.append((start,None))
    while open:
        current = min(open, key=lambda node: node[1])
        open.remove(current)
        if current[0] == goal:
            path = backtrack_path(closed,goal)
            print("Goal reached:", current[0])
            print("Path:", " -> ".join(path))
            return
        for neighbor, _ in graph[current[0]]:
            if neighbor not in [node for node, parent in closed] and neighbor not in [n for n,m in open]:
                open.append((neighbor, heuristic[neighbor]))
                closed.append((neighbor,current[0]))

    print("Goal not reachable")