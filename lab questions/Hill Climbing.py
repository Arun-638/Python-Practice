import random
graph = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
def calculate_cost(tour):
    cost = 0
    for i in range(len(tour)-1):
        cost+=graph[tour[i]][tour[i+1]]
    cost+=graph[tour[-1]][tour[0]]
    return cost
def neighbor(tour):
    neighbors = []
    for i in range(len(tour)):
        for j in range(i+1,len(tour)):
            new_tour = tour.copy()
            new_tour[i],new_tour[j] = new_tour[j],new_tour[i]
            neighbors.append(new_tour)
    return neighbors
def hill_climbing():
    tour = list(range(len(graph)))
    random.shuffle(tour)
    current_cost = calculate_cost(tour)
    while True:
        neighbors = neighbor(tour)
        best_neighbor = None
        best_cost = current_cost
        for n in neighbors:
            cost = calculate_cost(n)
            if cost < best_cost:
                best_cost = cost
                best_neighbor = n
        if best_neighbor is None:
            break
        tour = best_neighbor
        current_cost = best_cost
    return tour, current_cost
best_tour, best_cost = hill_climbing()
print("Best tour:", best_tour)
print("Best cost:", best_cost)