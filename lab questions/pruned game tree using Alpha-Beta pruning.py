import math
values = [5, 3, 2, 4, 1, 3, 6, 2, 8, 7, 5, 1, 3, 4]

def minimax(depth, is_maximizing, index, alpha, beta):
    if depth == 4:
        if index < len(values):
            print("Leaf:", values[index])
            return values[index]
        else:
            return 0 

    if is_maximizing:
        max_eval = -math.inf
        for i in reversed(range(2)):
            eval = minimax(depth + 1, False, index * 2 + i, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                print("Pruned at MAX node")
                break
        return max_eval

    else: 
        min_eval = math.inf
        for i in reversed(range(2)):
            eval = minimax(depth + 1, True, index * 2 + i, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                print("Pruned at MIN node")
                break
        return min_eval
result = minimax(0, False, 0, -math.inf, math.inf)

print("\nFinal Root Value:", result)