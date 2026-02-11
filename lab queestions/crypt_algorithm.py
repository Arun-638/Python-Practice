''' A crypt-arithmetic puzzle is a type of mathematical puzzle in 
which digits are assigned to 
alphabetical letters or symbols. The end goal is to find the unique 
digit assignment to each 
letter so that the given mathematical operation holds true. 
Solve the puzzles  
i) EAT + THAT = APPLE  
ii) POINT + ZERO = ENERGY 
iii) CROSS + ROADS = DANGER '''
#SOLVE THIS PUZZLE USING AC 3 ALGORITHM + Backtracking
puzzles = [
    ('EAT','THAT','APPLE'),
    ('POINT','ZERO','ENERGY'),
    ('CROSS','ROADS','DANGER')
]

digits = list(range(10))

def make_variables(puzzle):
    vars = {}
    for word in puzzle:
        for ch in word:
            if ch not in vars:
                vars[ch] = digits[:]    
    return vars

def ac3(csp):
    queue = [(xi, xj) for xi in csp for xj in csp if xi != xj]
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp[xi]:
                return False
            for xk in csp:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    revised = False
    if len(csp[xj]) == 1:
        val = csp[xj][0]
        if val in csp[xi]:
            csp[xi].remove(val)
            revised = True
    return revised

def backtrack(csp, assignment, puzzle):
    if len(assignment) == len(csp):
        if arithmetic_ok(puzzle, assignment):
            return assignment
        return False
    
    var = select_unassigned_variable(csp, assignment)
    for value in csp[var]:
        if is_consistent(var, value, assignment) and not (value == 0 and is_leading(var, puzzle)):
            assignment[var] = value
            result = backtrack(csp, assignment, puzzle)
            if result:
                return result
            del assignment[var]
    return False

def select_unassigned_variable(csp, assignment):
    for var in csp:
        if var not in assignment:
            return var

def is_consistent(var, value, assignment):
    return value not in assignment.values()

def is_leading(var, puzzle):
    for word in puzzle:
        if word[0] == var:
            return True
    return False

def arithmetic_ok(puzzle, assignment):
    if len(assignment) < len(set(''.join(puzzle))):
        return True
    
    w1, w2, w3 = puzzle
    n1 = int("".join(str(assignment[c]) for c in w1))
    n2 = int("".join(str(assignment[c]) for c in w2))
    n3 = int("".join(str(assignment[c]) for c in w3))
    return n1 + n2 == n3

for puzzle in puzzles:
    csp = make_variables(puzzle)
    if ac3(csp):
        solution = backtrack(csp, {}, puzzle)
        if solution:
            print(f"Solution for {puzzle}: {solution}")
        else:
            print(f"No solution found for {puzzle}")
    else:
        print(f"No solution found for {puzzle} using AC-3")

