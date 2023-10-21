class Move:
    row_to_rank = {row: str(8 - row) for row in range(8)}
    col_to_file = {col: chr(97 + col) for col in range(8)}

    def __init__(self, start_square, end_square, board):
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_rank_file(self, row, col):
        return self.col_to_file.get(col) + self.row_to_rank.get(row)

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(
            self.end_row, self.end_col
        )
