import random
graph = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
def calculate_cost(tour):
    cost = 0
    for i in range(len(tour) - 1):
        cost += graph[tour[i]][tour[i + 1]]
    cost += graph[tour[-1]][tour[0]]
    return cost
def get_neighbors(tour):
    neighbors = []
    for i in range(len(tour)):
        for j in range(i + 1, len(tour)):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i] 
            neighbors.append(neighbor)
    return neighbors
def hill_climbing():
    tour = list(range(len(graph)))
    random.shuffle(tour)
    current_cost = calculate_cost(tour)
    
    while True:
        neighbors = get_neighbors(tour)
        next_tour = None
        next_cost = current_cost
        
        for neighbor in neighbors:
            cost = calculate_cost(neighbor)
            if cost < next_cost:
                next_tour = neighbor
                next_cost = cost
        
        if next_tour is None: 
            break
        
        tour = next_tour
        current_cost = next_cost
    
    return tour, current_cost
best_tour, best_cost = hill_climbing()
print("Best tour found:", best_tour)
print("Cost of the best tour:", best_cost)
