import itertools

from src.moves import Move


class GameState:
    DIMENSION = 8

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_funcs = {
            "P": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves,
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.check_mate = False
        self.stale_mate = False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        # King Move
        if move.piece_moved == "wK":
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # Undo King Move
            if move.piece_moved == "wK":
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_loc = (move.start_row, move.start_col)

    def get_valid_moves(self):
        moves = self.all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_loc)
        return self.square_under_attack(self.black_king_loc)

    def square_under_attack(self, location):
        self.white_to_move = not self.white_to_move
        oop_moves = self.all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in oop_moves:
            if (move.end_row, move.end_col) == location:
                return True
        return False

    def all_possible_moves(self):
        moves = []
        for row, col in itertools.product(range(self.DIMENSION), range(self.DIMENSION)):
            turn, piece = self.board[row][col][:2]
            if (turn == "w" and self.white_to_move) or (
                turn == "b" and not self.white_to_move
            ):
                self.move_funcs.get(piece)(row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            # Pawn Advance 1 Square Chk
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                # Pawn Advance 2 Square Chk
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))

            # Check left piece capture
            if col >= 1 and self.board[row - 1][col - 1].startswith("b"):
                moves.append(Move((row, col), (row - 1, col - 1), self.board))

            # Check right piece capture
            if col <= 6 and self.board[row - 1][col + 1].startswith("b"):
                moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            # Pawn Advance 1 Square Chk
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                # Pawn Advance 2 Square Chk
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))

            # Check left piece capture
            if col >= 1 and self.board[row + 1][col - 1].startswith("w"):
                moves.append(Move((row, col), (row + 1, col - 1), self.board))

            # Check right piece capture
            if col <= 6 and self.board[row + 1][col + 1].startswith("w"):
                moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        row_col_direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy = "b" if self.white_to_move else "w"

        for direction in row_col_direction:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    next_piece = self.board[end_row][end_col]
                    if next_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif next_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        row_col_move = [
            (1, 2),
            (2, 1),
            (-1, -2),
            (-2, -1),
            (-1, 2),
            (1, -2),
            (-2, 1),
            (2, -1),
        ]
        ally = "w" if self.white_to_move else "b"
        for m in row_col_move:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                next_piece = self.board[end_row][end_col]
                if next_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        row_col_direction = [(-1, 1), (1, -1), (1, 1), (-1, -1)]
        enemy = "b" if self.white_to_move else "w"
        for direction in row_col_direction:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    next_piece = self.board[end_row][end_col]
                    if next_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif next_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        row_col_move = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
            (-1, -1),
        ]
        ally = "w" if self.white_to_move else "b"
        for m in row_col_move:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                next_piece = self.board[end_row][end_col]
                if next_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
