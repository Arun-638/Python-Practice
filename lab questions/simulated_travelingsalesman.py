import random
import math

graph = [
    [0,10,15,20],
    [10,0,35,25],
    [15,35,0,30],
    [20,25,30,0]
]

def calculate_cost(tour):
    cost = 0
    for i in range(len(tour)-1):
        cost += graph[tour[i]][tour[i+1]]
    cost += graph[tour[-1]][tour[0]]
    return cost

def get_neighbor(tour):
    new_tour = tour.copy()
    i = random.randint(0,len(tour)-1)
    j = random.randint(0,len(tour)-1)
    while i == j:
        j = random.randint(0,len(tour)-1)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


def simulated_annealing():
    tour = list(range(len(graph)))
    random.shuffle(tour)
    current_cost = calculate_cost(tour)
    best_tour = tour.copy()
    best_cost = current_cost
    temperature = 1000
    cooling_rate = 0.95
    while temperature > 1:
        new_tour = get_neighbor(tour)
        new_cost = calculate_cost(new_tour)
        difference = new_cost - current_cost
        if difference < 0:
            tour = new_tour
            current_cost = new_cost

        else:
            probability = math.exp(-difference / temperature)

            if random.random() < probability:
                tour = new_tour
                current_cost = new_cost

        if current_cost < best_cost:
            best_tour = tour.copy()
            best_cost = current_cost

        temperature *= cooling_rate

    return best_tour, best_cost


best_tour, best_cost = simulated_annealing()

print("Best tour:", best_tour)
print("Best cost:", best_cost)