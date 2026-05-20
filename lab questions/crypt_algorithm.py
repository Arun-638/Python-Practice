def is_consistent(assignment, value, letter):
    # same digit should not be assigned to different letters
    for l, v in assignment.items():
        if v == value and l != letter:
            return False
    return True


def check_sum(assignment, word1, word2, result):
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
        return None

    letter = variables[len(assignment)]

    for value in domains[letter]:
        if is_consistent(assignment, value, letter):
            assignment[letter] = value

            solution = backtrack(assignment, variables, domains, word1, word2, result)

            if solution is not None:
                return solution

            del assignment[letter]

    return None


def solve_cryptarithmetic(word1, word2, result):
    print("\nSolving:", word1, "+", word2, "=", result)

    variables = []

    for letter in word1 + word2 + result:
        if letter not in variables:
            variables.append(letter)

    domains = {}

    for letter in variables:
        domains[letter] = list(range(10))

    # first letters cannot be zero
    for first in [word1[0], word2[0], result[0]]:
        if 0 in domains[first]:
            domains[first].remove(0)

    solution = backtrack({}, variables, domains, word1, word2, result)

    if solution is None:
        print("No solution found.")
    else:
        print("Solution:", solution)


solve_cryptarithmetic("EAT", "THAT", "APPLE")
solve_cryptarithmetic("POINT", "ZERO", "ENERGY")
solve_cryptarithmetic("CROSS", "ROADS", "DANGER")