''' A crypt-arithmetic puzzle is a type of mathematical puzzle in 
which digits are assigned to 
alphabetical letters or symbols. The end goal is to find the unique 
digit assignment to each 
letter so that the given mathematical operation holds true. 
Solve the puzzles  
i) EAT + THAT = APPLE  
ii) POINT + ZERO = ENERGY 
iii) CROSS + ROADS = DANGER '''
#AC 3
def revise(domains, xi, xj):
    if len(domains[xj]) == 1:
        value = domains[xj][0]
        if value in domains[xi]:
            domains[xi].remove(value)
            return True
    return False
def ac3(domains,variables):
    queue = []
    for xi in variables:
        for xj in variables:
            if xi != xj and (xi,xj) not in queue:
                queue.append((xi,xj))
    while queue:
        (xi,xj) = queue.pop(0)
        if revise(domains,xi,xj):
            if not domains[xi]:
                return False
            for xk in variables:
                if xk != xi and xk != xj and (xk,xi) not in queue:
                    queue.append((xk,xi))
    return True
#backtracking
def select_unassigned_variable(assignment, variables, domains):
    unassigned = [v for v in variables if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

def is_consistent(assignment,value,letter):
    for l,v in assignment.items():
        if v == value and l != letter:
            return False
    return True
def check_sum(assignment,word1,word2,result):
    def word_number(word):
        number = 0
        for letter in word:
            number = number * 10 + assignment[letter]
        return number
    return word_number(word1) + word_number(word2) == word_number(result)
def backtrack(assignment, variables, domains, word1, word2, result):
    if len(assignment) == len(variables):
        if check_sum(assignment, word1, word2, result):
            return assignment
        else:
            return "failure"
    letter = select_unassigned_variable(assignment, variables,domains)
    for value in domains[letter]:
        if is_consistent(assignment, value,letter):
            assignment[letter] = value
            solution = backtrack(assignment, variables, domains, word1, word2, result)
            if solution != "failure":
                return solution
            del assignment[letter]
    return "failure"
def solve_cryptarithmetic(word1, word2, result):
    print("Solving: ", word1, "+", word2, "=", result)
    variables = []
    for letter in word1 + word2 + result:
        if letter not in variables:
            variables.append(letter)
    domains = {}
    for letter in variables:
        domains[letter] = list(range(10))
    for first in [word1[0], word2[0], result[0]]:
        if 0 in domains[first]:
            domains[first].remove(0)
    if not ac3(domains, variables):
        print("No solution found.")
        return
    assignment = {}
    solution = backtrack(assignment, variables, domains, word1, word2, result)
    if solution == "failure":
        print("No solution found.")
    else:
        print("Solution: ", solution)
solve_cryptarithmetic("EAT", "THAT", "APPLE")
solve_cryptarithmetic("POINT", "ZERO", "ENERGY")
solve_cryptarithmetic("CROSS", "ROADS", "DANGER")