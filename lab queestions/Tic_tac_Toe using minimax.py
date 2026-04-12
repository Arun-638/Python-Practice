import math

board = ['-'] * 9

def print_board(board):
    for i in range(3):
        print(board[3*i], board[3*i+1], board[3*i+2])
    print()

def check_winner(board):
    winning_combinations = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '-':
            return board[combo[0]]
    return None

def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)

    if winner == 'O':
        return 10 - depth
    elif winner == 'X':
        return depth - 10
    elif '-' not in board:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = 'O'
                score = minimax(board, depth+1, False, alpha, beta)
                board[i] = '-'
                
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = 'X'
                score = minimax(board, depth+1, True, alpha, beta)
                board[i] = '-'
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_score

def best_move(board):
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == '-':
            board[i] = 'O'
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = '-'

            if score > best_score:
                best_score = score
                move = i

    return move

def play_game():
    print_board(board)

    while True:
        move = int(input("Enter your move (0-8): "))

        if board[move] == '-':
            board[move] = 'X'
            print_board(board)

            if check_winner(board) == 'X':
                print("You win!")
                break
            elif '-' not in board:
                print("It's a draw!")
                break

            computer_move = best_move(board)
            board[computer_move] = 'O'
            print("Computer's move:")
            print_board(board)

            if check_winner(board) == 'O':
                print("Computer wins!")
                break
            elif '-' not in board:
                print("It's a draw!")
                break

play_game()