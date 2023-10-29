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
        self.in_check = False
        self.pins = []
        self.checks = []

    def make_move(self, move):
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = "--"
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
        moves = []
        self.in_check, self.pins, self.checks = self.get_pins_check()

        king_row, king_col = list(
            self.white_king_loc if self.white_to_move else self.black_king_loc
        )
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.all_possible_moves()
                check_info = self.checks[0]
                check_row, check_col, dir_x, dir_y = check_info
                piece_type = self.board[check_row][check_col][1]
                valid_squares = []
                if piece_type == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + dir_x * i, king_col + dir_y * i)
                        valid_squares.append(valid_square)
                        if valid_square == (check_row, check_col):
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if (
                        moves[i].piece_moved[1] != "K"
                        and not (moves[i].end_row, moves[i].end_col) in valid_squares
                    ):
                        moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.all_possible_moves()
        return moves

    def all_possible_moves(self):
        moves = []
        for row, col in itertools.product(range(self.DIMENSION), range(self.DIMENSION)):
            turn, piece = self.board[row][col][:2]
            if (turn == "w" and self.white_to_move) or (
                turn == "b" and not self.white_to_move
            ):
                self.move_funcs.get(piece)(row, col, moves)
        return moves

    def get_pins_check(self):
        pins, checks = [], []
        in_check = False
        if self.white_to_move:
            enemy_color, ally_color = "b", "w"
            start_row, start_col = self.white_king_loc
        else:
            enemy_color, ally_color = "w", "b"
            start_row, start_col = self.black_king_loc
        directions = (
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        )
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                # Out of boarf
                if not 0 <= end_row <= 7 or not 0 <= end_col <= 7:
                    break
                end_piece = self.board[end_row][end_col]
                piece_color, piece_type = list(end_piece)
                # Pin Check
                if piece_color == ally_color and piece_type != "K":
                    if possible_pin == ():
                        possible_pin = (end_row, end_col, d[0], d[1])
                    else:
                        break
                # Check for possible checks for Pawn, Rook, Bishop, King, Queen
                elif piece_color == enemy_color:
                    if (
                        (0 <= j <= 3 and piece_type == "R")
                        or (4 <= j <= 7 and piece_type == "B")
                        or (piece_type == "Q")
                        or (i == 1 and piece_type == "K")
                        or (
                            i == 1
                            and piece_type == "P"
                            and (
                                (enemy_color == "w" and 6 <= j <= 7)
                                or (enemy_color == "b" and 4 <= j <= 5)
                            )
                        )
                    ):
                        if possible_pin == ():
                            in_check = True
                            checks.append((end_row, end_col, d[0], d[1]))
                        else:
                            pins.append(possible_pin)
                    break
        # Check for possible checks for Knight
        knight_directions = [
            (1, 2),
            (2, 1),
            (-1, -2),
            (-2, -1),
            (-1, 2),
            (1, -2),
            (-2, 1),
            (2, -1),
        ]
        for m in knight_directions:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                piece_color, piece_type = list(end_piece)
                if piece_color == enemy_color and piece_type == "N":
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        return in_check, pins, checks

    def get_pawn_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            r, c, x, y = self.pins[i]
            if r == row and c == col:
                piece_pinned = True
                pin_direction = (x, y)
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            # Pawn Advance 1 Square Chk
            if self.board[row - 1][col] == "--" and (
                not piece_pinned or pin_direction == (-1, 0)
            ):
                moves.append(Move((row, col), (row - 1, col), self.board))
                # Pawn Advance 2 Square Chk
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))

            # Check left piece capture
            if (
                col >= 1
                and self.board[row - 1][col - 1].startswith("b")
                and (not piece_pinned or pin_direction == (-1, -1))
            ):
                moves.append(Move((row, col), (row - 1, col - 1), self.board))

            # Check right piece capture
            if (
                col <= 6
                and self.board[row - 1][col + 1].startswith("b")
                and (not piece_pinned or pin_direction == (-1, 1))
            ):
                moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            # Pawn Advance 1 Square Chk
            if self.board[row + 1][col] == "--" and (
                not piece_pinned or pin_direction == (1, 0)
            ):
                moves.append(Move((row, col), (row + 1, col), self.board))
                # Pawn Advance 2 Square Chk
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))

            # Check left piece capture
            if (
                col >= 1
                and self.board[row + 1][col - 1].startswith("w")
                and (not piece_pinned or pin_direction == (1, -1))
            ):
                moves.append(Move((row, col), (row + 1, col - 1), self.board))

            # Check right piece capture
            if (
                col <= 6
                and self.board[row + 1][col + 1].startswith("w")
                and (not piece_pinned or pin_direction == (1, 1))
            ):
                moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            r, c, x, y = self.pins[i]
            if r == row and c == col:
                piece_pinned = True
                pin_direction = (x, y)
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        row_col_direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy = "b" if self.white_to_move else "w"

        for direction in row_col_direction:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if (
                    0 <= end_row <= 7
                    and 0 <= end_col <= 7
                    and (
                        not piece_pinned
                        or pin_direction == direction
                        or pin_direction == (-direction[0], -direction[1])
                    )
                ):
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
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            r, c = self.pins[i][:2]
            if r == row and c == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

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
            if 0 <= end_row <= 7 and 0 <= end_col <= 7 and not piece_pinned:
                next_piece = self.board[end_row][end_col]
                if next_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            r, c, x, y = self.pins[i]
            if r == row and c == col:
                piece_pinned = True
                pin_direction = (x, y)
                self.pins.remove(self.pins[i])
                break

        row_col_direction = [(-1, 1), (1, -1), (1, 1), (-1, -1)]
        enemy = "b" if self.white_to_move else "w"
        for direction in row_col_direction:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if (
                    0 <= end_row <= 7
                    and 0 <= end_col <= 7
                    and (
                        not piece_pinned
                        or pin_direction == direction
                        or pin_direction == (-direction[0], -direction[1])
                    )
                ):
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
        ally_color = "w" if self.white_to_move else "b"
        for m in row_col_move:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                next_piece = self.board[end_row][end_col]
                if next_piece[0] != ally_color:
                    if ally_color == "w":
                        self.white_king_loc = (end_row, end_col)
                    else:
                        self.black_king_loc = (end_row, end_col)

                    in_check, pins, checks = self.get_pins_check()

                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    if ally_color == "w":
                        self.white_king_loc = (row, col)
                    else:
                        self.black_king_loc = (row, col)
