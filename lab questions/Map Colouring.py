domain = ["red", "green", "blue"]
variables = {"WA" : ["NT", "SA"], "NT" : ["WA", "SA", "Q"], "SA" : ["WA", "NT", "Q", "NSW", "V"], "Q" : ["NT", "SA", "NSW"], "NSW" : ["SA", "Q", "V"], "V" : ["SA", "NSW"]}
def map_colouring(variables, domains):
    assignment = {}
    if backtracking(assignment, variables, domains):
        return assignment
    else:
        return None

def backtracking(assignment, variables, domains):
    if len(assignment) == len(variables):
        return True
    var = select_unassigned_variable(assignment, variables)
    for value in domains:
        if is_consistent(assignment,var,value):
            assignment[var] = value
            if backtracking(assignment, variables, domains):
                return True
            del assignment[var]
    return False

def select_unassigned_variable(assignment, variables):
    for var in variables:
        if var not in assignment:
            return var
    return None
def is_consistent(assignment, var, value):
    for neighbor in variables[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True
result = map_colouring(variables, domain)
if result:
    print("Solution found:")
    for var in result:
        print(f"{var}: {result[var]}")
else:    print("No solution found.")
