# X is Me
# O is the Computer
board = ['-'] * 9
queue = []
visited = []
def print_board(current):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print()
        print(current[i], end=" ")
    print()
def check_winner(current):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    for i in winning_combinations:
        if current[i[0]] == current[i[1]] == current[i[2]] == 'X':
            return 'X'
        if current[i[0]] == current[i[1]] == current[i[2]] == 'O':
            return 'O'
    return None
def start_game(current):
    print_board(current)
    queue.append(current)
    visited.append(current)
    while queue:
        current = queue.pop(0)
        winner = check_winner(current)
        if winner:
            print(f"{winner} wins!")
            print()
            print_board(current)
            break
        move = int(input("Enter your move (0-8): "))
        if current[move] == '-':
            current[move] = 'X'
            print_board(current)
            if '-' not in current:
                print("It's a draw!")
                return
            for i in range(9):
                if current[i] == '-':
                    new_board = current[:]
                    new_board[i] = 'O'
                    if new_board not in visited:
                        visited.append(new_board)
                        queue.append(new_board)
                    print("Computer's move:")
                    print_board(new_board)
                    break
        else:
            print("Invalid move. Try again.")
start_game(board)