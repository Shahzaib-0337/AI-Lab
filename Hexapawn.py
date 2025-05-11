import pygame
import numpy as np
import sys
import time
from copy import deepcopy

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
YELLOW = (255, 255, 0)  # For selected piece highlight

# Font
FONT = pygame.font.SysFont('Arial', 32)

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HexaPawn: Strategic Variant with Enhanced AI')

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, is_blocker=False):
        self.row = row
        self.col = col
        self.color = color
        self.is_blocker = is_blocker
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        if self.is_blocker:
            # Draw blocker as a square
            pygame.draw.rect(win, BROWN, (self.x - SQUARE_SIZE//2 + self.PADDING, 
                                        self.y - SQUARE_SIZE//2 + self.PADDING, 
                                        SQUARE_SIZE - 2*self.PADDING, 
                                        SQUARE_SIZE - 2*self.PADDING))
        else:
            # Draw pawn as a circle
            pygame.draw.circle(win, self.color, (self.x, self.y), radius)
            pygame.draw.circle(win, BLACK, (self.x, self.y), radius, self.OUTLINE)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

class Board:
    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 4
        self.white_blockers = self.black_blockers = 1
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, GRAY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    self.board[row].append(Piece(row, col, BLACK))
                elif row == ROWS - 1:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row == 1 and col == 1:
                    self.board[row].append(Piece(row, col, BLACK, True))
                elif row == ROWS - 2 and col == COLS - 2:
                    self.board[row].append(Piece(row, col, WHITE, True))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE:
            # White pawn moves (moving up the board)
            if piece.is_blocker:
                return moves  # Blockers can't move
            
            # Forward move
            if row - 1 >= 0:
                if self.board[row - 1][piece.col] == 0:
                    moves[(row - 1, piece.col)] = "move"
                # Capture left
                if left >= 0 and self.board[row - 1][left] != 0 and self.board[row - 1][left].color != piece.color and not self.board[row - 1][left].is_blocker:
                    moves[(row - 1, left)] = "capture"
                # Capture right
                if right < COLS and self.board[row - 1][right] != 0 and self.board[row - 1][right].color != piece.color and not self.board[row - 1][right].is_blocker:
                    moves[(row - 1, right)] = "capture"
            
            # Push mechanics for white
            if row - 1 >= 0 and piece.col + 1 < COLS:
                if (self.board[row][piece.col + 1] != 0 and 
                    self.board[row][piece.col + 1].color == WHITE and 
                    not self.board[row][piece.col + 1].is_blocker and
                    self.board[row - 1][piece.col + 1] != 0 and 
                    self.board[row - 1][piece.col + 1].is_blocker and
                    self.board[row - 1][piece.col + 1].color != WHITE):
                    moves[(row - 1, piece.col + 1)] = "push"
            
            if row - 1 >= 0 and piece.col - 1 >= 0:
                if (self.board[row][piece.col - 1] != 0 and 
                    self.board[row][piece.col - 1].color == WHITE and 
                    not self.board[row][piece.col - 1].is_blocker and
                    self.board[row - 1][piece.col - 1] != 0 and 
                    self.board[row - 1][piece.col - 1].is_blocker and
                    self.board[row - 1][piece.col - 1].color != WHITE):
                    moves[(row - 1, piece.col - 1)] = "push"

        else:
            # Black pawn moves (moving down the board)
            if piece.is_blocker:
                return moves  # Blockers can't move
            
            # Forward move
            if row + 1 < ROWS:
                if self.board[row + 1][piece.col] == 0:
                    moves[(row + 1, piece.col)] = "move"
                # Capture left
                if left >= 0 and self.board[row + 1][left] != 0 and self.board[row + 1][left].color != piece.color and not self.board[row + 1][left].is_blocker:
                    moves[(row + 1, left)] = "capture"
                # Capture right
                if right < COLS and self.board[row + 1][right] != 0 and self.board[row + 1][right].color != piece.color and not self.board[row + 1][right].is_blocker:
                    moves[(row + 1, right)] = "capture"
            
            # Push mechanics for black
            if row + 1 < ROWS and piece.col + 1 < COLS:
                if (self.board[row][piece.col + 1] != 0 and 
                    self.board[row][piece.col + 1].color == BLACK and 
                    not self.board[row][piece.col + 1].is_blocker and
                    self.board[row + 1][piece.col + 1] != 0 and 
                    self.board[row + 1][piece.col + 1].is_blocker and
                    self.board[row + 1][piece.col + 1].color != BLACK):
                    moves[(row + 1, piece.col + 1)] = "push"
            
            if row + 1 < ROWS and piece.col - 1 >= 0:
                if (self.board[row][piece.col - 1] != 0 and 
                    self.board[row][piece.col - 1].color == BLACK and 
                    not self.board[row][piece.col - 1].is_blocker and
                    self.board[row + 1][piece.col - 1] != 0 and 
                    self.board[row + 1][piece.col - 1].is_blocker and
                    self.board[row + 1][piece.col - 1].color != BLACK):
                    moves[(row + 1, piece.col - 1)] = "push"

        return moves

    def winner(self):
        # Check if white reached the top row
        for col in range(COLS):
            if self.board[0][col] != 0 and self.board[0][col].color == WHITE and not self.board[0][col].is_blocker:
                return WHITE
        
        # Check if black reached the bottom row
        for col in range(COLS):
            if self.board[ROWS - 1][col] != 0 and self.board[ROWS - 1][col].color == BLACK and not self.board[ROWS - 1][col].is_blocker:
                return BLACK
        
        # Check if all white pawns are gone
        white_pawns = 0
        black_pawns = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and not piece.is_blocker:
                    if piece.color == WHITE:
                        white_pawns += 1
                    else:
                        black_pawns += 1
        
        if white_pawns == 0:
            return BLACK
        if black_pawns == 0:
            return WHITE
        
        return None

    def has_legal_moves(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color and not piece.is_blocker:
                    if len(self.get_valid_moves(piece)) > 0:
                        return True
        return False

    def ai_move(self, board):
        start_time = time.time()
        best_move = None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        max_depth = 4  # Limit the search depth
        
        # Get all possible moves for black
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece != 0 and piece.color == BLACK and not piece.is_blocker:
                    moves = board.get_valid_moves(piece)
                    for move, move_type in moves.items():
                        new_row, new_col = move
                        temp_board = deepcopy(board)
                        temp_piece = temp_board.get_piece(row, col)
                        
                        # Make the move on the temp board
                        if move_type == "move":
                            temp_board.move(temp_piece, new_row, new_col)
                        elif move_type == "capture":
                            temp_board.board[new_row][new_col] = 0
                            temp_board.move(temp_piece, new_row, new_col)
                            temp_board.white_left -= 1
                        elif move_type == "push":
                            temp_board.board[new_row][new_col] = 0
                            temp_board.move(temp_piece, new_row, new_col)
                            temp_board.white_blockers -= 1
                        
                        # Evaluate the move
                        board_value = self.minimax(temp_board, max_depth, False, alpha, beta, max_depth)
                        
                        if board_value > best_value:
                            best_value = board_value
                            best_move = (piece, move, move_type)
        
        end_time = time.time()
        print(f"AI move took {end_time - start_time:.2f} seconds")
        
        if best_move:
            piece, move, move_type = best_move
            new_row, new_col = move
            if move_type == "move":
                self.move(piece, new_row, new_col)
            elif move_type == "capture":
                self.board[new_row][new_col] = 0
                self.move(piece, new_row, new_col)
                self.white_left -= 1
            elif move_type == "push":
                self.board[new_row][new_col] = 0
                self.move(piece, new_row, new_col)
                self.white_blockers -= 1
            return True
        return False

    def minimax(self, board, depth, maximizing_player, alpha, beta, max_depth=4):
        # Base cases
        winner = board.winner()
        if winner == BLACK:
            return float('inf')
        elif winner == WHITE:
            return -float('inf')
        elif depth == 0 or not board.has_legal_moves(BLACK if maximizing_player else WHITE):
            return self.evaluate(board)
        
        # Prevent infinite recursion
        if depth > max_depth:
            return self.evaluate(board)
        
        if maximizing_player:
            max_eval = -float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    piece = board.board[row][col]
                    if piece != 0 and piece.color == BLACK and not piece.is_blocker:
                        moves = board.get_valid_moves(piece)
                        for move, move_type in moves.items():
                            new_row, new_col = move
                            temp_board = deepcopy(board)
                            temp_piece = temp_board.get_piece(row, col)
                            
                            if move_type == "move":
                                temp_board.move(temp_piece, new_row, new_col)
                            elif move_type == "capture":
                                temp_board.board[new_row][new_col] = 0
                                temp_board.move(temp_piece, new_row, new_col)
                                temp_board.white_left -= 1
                            elif move_type == "push":
                                temp_board.board[new_row][new_col] = 0
                                temp_board.move(temp_piece, new_row, new_col)
                                temp_board.white_blockers -= 1
                            
                            evaluation = self.minimax(temp_board, depth - 1, False, alpha, beta, max_depth)
                            max_eval = max(max_eval, evaluation)
                            alpha = max(alpha, evaluation)
                            if beta <= alpha:
                                break
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    piece = board.board[row][col]
                    if piece != 0 and piece.color == WHITE and not piece.is_blocker:
                        moves = board.get_valid_moves(piece)
                        for move, move_type in moves.items():
                            new_row, new_col = move
                            temp_board = deepcopy(board)
                            temp_piece = temp_board.get_piece(row, col)
                            
                            if move_type == "move":
                                temp_board.move(temp_piece, new_row, new_col)
                            elif move_type == "capture":
                                temp_board.board[new_row][new_col] = 0
                                temp_board.move(temp_piece, new_row, new_col)
                                temp_board.black_left -= 1
                            elif move_type == "push":
                                temp_board.board[new_row][new_col] = 0
                                temp_board.move(temp_piece, new_row, new_col)
                                temp_board.black_blockers -= 1
                            
                            evaluation = self.minimax(temp_board, depth - 1, True, alpha, beta, max_depth)
                            min_eval = min(min_eval, evaluation)
                            beta = min(beta, evaluation)
                            if beta <= alpha:
                                break
                        if beta <= alpha:
                            break
            return min_eval

    def evaluate(self, board):
        # Piece values
        pawn_value = 1
        blocker_value = 2
        
        # Material score
        white_score = 0
        black_score = 0
        
        # Count pieces and calculate material score
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece != 0:
                    if piece.color == WHITE:
                        if piece.is_blocker:
                            white_score += blocker_value
                        else:
                            white_score += pawn_value
                            # Add positional bonus for white pieces
                            white_score += (ROWS - row) * 0.1  # Closer to promotion is better
                    else:
                        if piece.is_blocker:
                            black_score += blocker_value
                        else:
                            black_score += pawn_value
                            # Add positional bonus for black pieces
                            black_score += row * 0.1  # Closer to promotion is better
        
        # Center control bonus
        center_squares = [(1,1), (1,2), (2,1), (2,2)]
        for (row, col) in center_squares:
            piece = board.board[row][col]
            if piece != 0:
                if piece.color == WHITE:
                    white_score += 0.2
                else:
                    black_score += 0.2
        
        # Mobility score (weighted more heavily)
        white_moves = 0
        black_moves = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.board[row][col]
                if piece != 0 and not piece.is_blocker:
                    moves = board.get_valid_moves(piece)
                    if piece.color == WHITE:
                        white_moves += len(moves)
                    else:
                        black_moves += len(moves)
        
        white_score += white_moves * 0.15
        black_score += black_moves * 0.15
        
        # King safety (pieces near the back row)
        for col in range(COLS):
            if board.board[0][col] != 0 and board.board[0][col].color == WHITE:
                white_score += 0.3
            if board.board[ROWS-1][col] != 0 and board.board[ROWS-1][col].color == BLACK:
                black_score += 0.3
        
        return black_score - white_score

class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = WHITE
        self.selected = None
        self.valid_moves = {}
        self.game_over = False

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if self.selected:
            self.highlight_selected()
        pygame.display.update()

    def highlight_selected(self):
        row, col = self.selected.row, self.selected.col
        pygame.draw.rect(self.win, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        
        # If clicking on a piece of current turn, select it
        if piece != 0 and piece.color == self.turn and not piece.is_blocker:
            # If clicking on same piece, deselect it
            if self.selected and self.selected.row == row and self.selected.col == col:
                self.selected = None
                self.valid_moves = {}
            else:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves and (piece == 0 or piece.color != self.turn):
            move_type = self.valid_moves[(row, col)]
            
            if move_type == "move":
                self.board.move(self.selected, row, col)
            elif move_type == "capture":
                self.board.board[row][col] = 0
                self.board.move(self.selected, row, col)
                if self.turn == WHITE:
                    self.board.black_left -= 1
                else:
                    self.board.white_left -= 1
            elif move_type == "push":
                self.board.board[row][col] = 0  # Remove the blocker
                self.board.move(self.selected, row, col)
                if self.turn == WHITE:
                    self.board.black_blockers -= 1
                else:
                    self.board.white_blockers -= 1
            
            self.change_turn()
            return True
        return False

    def draw_valid_moves(self, moves):
        for move, move_type in moves.items():
            row, col = move
            color = GREEN if move_type == "move" else RED if move_type == "capture" else BLUE
            pygame.draw.circle(self.win, color, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def check_game_over(self):
        winner = self.board.winner()
        if winner is not None:
            self.game_over = True
            return winner
        
        # Check for draw (current player has no legal moves)
        current_color = self.turn
        if not self.board.has_legal_moves(current_color):
            self.game_over = True
            return "DRAW"
        
        return None

    def show_game_over(self, result):
        if result == WHITE:
            text = "White wins!"
        elif result == BLACK:
            text = "Black wins!"
        else:
            text = "Game ended in a draw!"
        
        text_surface = FONT.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Create a semi-transparent background
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((255, 255, 255, 128))
        self.win.blit(s, (0, 0))
        
        self.win.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)

    def ai_turn(self):
        if self.turn == BLACK and not self.game_over:
            moved = self.board.ai_move(self.board)
            if moved:
                self.change_turn()

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(60)
        
        game.ai_turn()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == WHITE and not game.game_over:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                
                if (row, col) in game.valid_moves:
                    game._move(row, col)
                    # Check if game ended after player move
                    result = game.check_game_over()
                    if result is not None:
                        game.show_game_over(result)
                        run = False
                else:
                    game.select(row, col)
        
        game.update()
        
        # Check if game ended after AI move
        if game.turn == WHITE:  # AI just moved
            result = game.check_game_over()
            if result is not None:
                game.show_game_over(result)
                run = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()