#tic tac toe using minimax algorithm and no alpha-beta pruning
import math
board = ['-'] * 9
def print_board(board):
    for i in range(3):
        print(board[3*i],board[3*i+1],board[3*i+2])
    print()
def check_winner(board):
    winning_combinations = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '-':
            return board[combo[0]]
    return None
def minimax(board, depth, is_maximizing):
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
                score = minimax(board, depth+1, False)
                board[i] = '-'
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = 'X'
                score = minimax(board, depth+1, True)
                board[i] = '-'
                best_score = min(score, best_score)
        return best_score
def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == '-':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = '-'
            if score > best_score:
                best_score = score
                move = i
    return move
while True:
    print_board(board)
    move = int(input("Enter your move (0-8): "))
    if board[move] == '-':
        board[move] = 'X'
    else:
        print("Invalid move. Try again.")
        continue
    if check_winner(board) == 'X':
        print_board(board)
        print("You win!")
        break
    elif '-' not in board:
        print_board(board)
        print("It's a draw!")
        break
    ai_move = best_move(board)
    if ai_move is not None:
        board[ai_move] = 'O'
    if check_winner(board) == 'O':
        print_board(board)
        print("AI wins!")
        break