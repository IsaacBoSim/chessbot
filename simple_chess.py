import chess
from chess_ai import ai_move

def display_board(board):
    print(board)

def player_move(board):
    move = input("Enter your move (in UCI format, e.g., e2e4): ")
    try:
        board.push_uci(move)
    except ValueError:
        print("Invalid move format or illegal move. Try again.")
        player_move(board)

def main():
    board = chess.Board()
    while not board.is_game_over():
        display_board(board)
        if board.turn == chess.WHITE:
            player_move(board)
        else:
            ai_move_result = ai_move(board)
            if ai_move_result:
                board.push(ai_move_result)

    print("Game over:", "Draw" if board.is_stalemate() or board.is_insufficient_material() else "Checkmate")

if __name__ == "__main__":
    main()

#cant promote
#cant end game check mate
#add sounds
#add piece move lag
#previous move color keep

