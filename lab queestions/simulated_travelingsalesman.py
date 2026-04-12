import random
import math

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

def calculate_cost(tour):
    cost = 0
    for i in range(len(tour) - 1):
        cost += graph[tour[i]][tour[i + 1]]

    cost += graph[tour[-1]][tour[0]]

    return cost


def get_neighbor(tour):
    new_tour = tour.copy()

    i = random.randint(0, len(tour) - 1)
    j = random.randint(0, len(tour) - 1)

    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

    return new_tour


def simulated_annealing():

    tour = list(range(len(graph)))
    random.shuffle(tour)

    current_cost = calculate_cost(tour)

    T = 1000
    cooling_rate = 0.95

    best_tour = tour.copy()
    best_cost = current_cost

    while T > 1:

        neighbor = get_neighbor(tour)
        neighbor_cost = calculate_cost(neighbor)

        diff = neighbor_cost - current_cost

        if diff < 0:
            tour = neighbor
            current_cost = neighbor_cost

        else:
            probability = math.exp(-diff / T)

            if random.random() < probability:
                tour = neighbor
                current_cost = neighbor_cost

        if current_cost < best_cost:
            best_tour = tour.copy()
            best_cost = current_cost

        T = T * cooling_rate

    return best_tour, best_cost


best_tour, best_cost = simulated_annealing()

print("Best tour found:", best_tour)
print("Cost of the best tour:", best_cost)