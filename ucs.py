graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5), ('C', 1)],
    'C': [('D', 1)],
    'D': []
}
def pop_min(frontier):
    min_index = 0
    for i in range(1, len(frontier)):
        if frontier[i][0] < frontier[min_index][0]:
            min_index = i
    return frontier.pop(min_index)


def uniform_cost_search(graph, start, goal):
    frontier = []
    visited = []

    frontier.append((0, start))  # (cost, node)

    while frontier:
        cost, node = pop_min(frontier)

        if node in visited:
            continue

        visited.append(node)

        if node == goal:
            print("Goal reached:", node)
            print("Total cost:", cost)
            return

        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                frontier.append((cost + edge_cost, neighbor))

    print("Goal not reachable")
