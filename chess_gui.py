import pygame
import chess
import sys
import random
from chess_ai import ai_move

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 550, 550
SQUARE_SIZE = WIDTH // 8
FONT_SIZE = 32

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

def load_images():
    pieces = {}
    for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
        pieces['w' + piece.upper()] = pygame.image.load(f'images/{piece.upper()}w.png').convert_alpha()
        pieces['b' + piece.upper()] = pygame.image.load(f'images/{piece.upper()}b.png').convert_alpha()
    return pieces

def draw_board(screen, board, pieces, player_color, selected_piece, last_move):
    colors = [pygame.Color('white'), pygame.Color('grey')]
    highlight_color = pygame.Color('yellow')

    for r in range(8):
        for c in range(8):
            color = colors[((r + c) % 2)]
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            #handle board flip if player is black
            if player_color == chess.WHITE:
                board_r, board_c = 7 - r, c
            else:
                board_r, board_c = r, 7 - c

            if selected_piece is not None and selected_piece == chess.square(board_c, board_r):
                pygame.draw.rect(screen, highlight_color, rect)

            if selected_piece is None and board.king(chess.WHITE) and board.is_check():
                pygame.draw.rect(screen, pygame.Color('red'), rect, 3)

            if last_move != None and last_move.from_square == chess.square(board_c, board_r):
                pygame.draw.rect(screen, pygame.Color('blue'), rect, 3)

            piece = board.piece_at(chess.square(board_c, board_r))
            if piece:
                piece_symbol = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
                screen.blit(pieces[piece_symbol], rect)

def draw_choice_window(screen, choices):
    font = pygame.font.Font(None, FONT_SIZE)
    screen.fill(pygame.Color('black'))
    y_offset = 100
    for choice in choices:
        text_surface = font.render(choice, True, pygame.Color('white'))
        rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text_surface, rect)
        y_offset += FONT_SIZE + 20
    pygame.display.flip()

def get_choice(choices):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y_offset = 100
                for i, choice in enumerate(choices):
                    rect = pygame.Rect(0, y_offset - FONT_SIZE // 2, WIDTH, FONT_SIZE + 20)
                    if rect.collidepoint(pos):
                        return choice
                    y_offset += FONT_SIZE + 20
        draw_choice_window(screen, choices)

def main():
    clock = pygame.time.Clock()
    pieces = load_images()
    board = chess.Board()
    running = True
    selected_piece = None
    last_move = None

    # Randomize player color
    player_color = random.choice([chess.WHITE, chess.BLACK])
    player_turn = player_color == chess.WHITE

    print(f"Player color: {'White' if player_color == chess.WHITE else 'Black'}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE

                if player_color == chess.WHITE:
                    board_col, board_row = col, 7 - row
                else:
                    board_col, board_row = 7 - col, row

                square = chess.square(board_col, board_row)
                print(f"Mouse clicked at: {pos}, corresponding square: {chess.square_name(square)}")

                if selected_piece is None:
                    if board.piece_at(square) and board.piece_at(square).color == player_color:
                        selected_piece = square
                        print(f"Selected piece at: {chess.square_name(selected_piece)}")
                else:
                    promotion = None
                    if board.piece_at(selected_piece).piece_type == chess.PAWN and board_row == 7:
                        choices = ['Queen', 'Rook', 'Bishop', 'Knight']
                        choice = get_choice(choices)
                        promotion = {'Queen': chess.QUEEN, 'Rook': chess.ROOK, 'Bishop': chess.BISHOP, 'Knight': chess.KNIGHT}[choice]
                    move = chess.Move(selected_piece, square, promotion=promotion)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_piece = None
                        player_turn = False
                        print(f"Moved piece to: {chess.square_name(square)}")
                        if board.is_checkmate():
                            print("Checkmate!")
                            running = False
                    else:
                        selected_piece = None
                        print("Invalid move")

        if not player_turn and not board.is_game_over():
            ai_move_result = ai_move(board)
            if ai_move_result:
                board.push(ai_move_result)
                print(f"AI moved: {ai_move_result.uci()}")
                if board.is_checkmate():
                    print("Checkmate!")
                    running = False
            player_turn = True
            last_move = ai_move_result

        screen.fill(pygame.Color('black'))
        draw_board(screen, board, pieces, player_color, selected_piece, last_move)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
