from assets import Black, White
import pygame as pg

pg.init()
WIDTH = 800
HEIGHT = 800
window = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Chess")
font = pg.font.Font("freesansbold.ttf", 20)
big_font = pg.font.Font("freesansbold.ttf", 50)
timer = pg.time.Clock()
fps = 60

white_pieces = {
    (0, 0): "Rook",
    (1, 0): "Knight",
    (2, 0): "Bishop",
    (3, 0): "King",
    (4, 0): "Queen",
    (5, 0): "Bishop",
    (6, 0): "Knight",
    (7, 0): "Rook",
    (0, 1): "Pawn",
    (1, 1): "Pawn",
    (2, 1): "Pawn",
    (3, 1): "Pawn",
    (4, 1): "Pawn",
    (5, 1): "Pawn",
    (6, 1): "Pawn",
    (7, 1): "Pawn",
}
black_pieces = {
    (0, 7): "Rook",
    (1, 7): "Knight",
    (2, 7): "Bishop",
    (3, 7): "Queen",
    (4, 7): "King",
    (5, 7): "Bishop",
    (6, 7): "Knight",
    (7, 7): "Rook",
    (0, 6): "Pawn",
    (1, 6): "Pawn",
    (2, 6): "Pawn",
    (3, 6): "Pawn",
    (4, 6): "Pawn",
    (5, 6): "Pawn",
    (6, 6): "Pawn",
    (7, 6): "Pawn",
}
white_captured_pieces, black_captured_pieces = [], []
# Piece Phase -> Phase
# 0 -> White
# 1 -> White Selects
# 2 -> Black
# 3 -> Black Selects
piece_phase = 0
piece_index = 100
valid_moves = []

# Load Pieces
# Black
black_king_load = pg.image.load(r"assets/Black/b_king.png")
black_king = pg.transform.scale(black_king_load, (100, 100))

black_queen_load = pg.image.load(r"assets/Black/b_queen.png")
black_queen = pg.transform.scale(black_queen_load, (100, 100))

black_rook_load = pg.image.load(r"assets/Black/b_rook.png")
black_rook = pg.transform.scale(black_rook_load, (100, 100))

black_knight_load = pg.image.load(r"assets/Black/b_knight.png")
black_knight = pg.transform.scale(black_knight_load, (100, 100))

black_bishop_load = pg.image.load(r"assets/Black/b_bishop.png")
black_bishop = pg.transform.scale(black_bishop_load, (100, 100))

black_pawn_load = pg.image.load(r"assets/Black/b_pawn.png")
black_pawn = pg.transform.scale(black_pawn_load, (100, 100))

# White
white_king_load = pg.image.load(r"assets/White/w_king.png")
white_king = pg.transform.scale(white_king_load, (100, 100))

white_queen_load = pg.image.load(r"assets/White/w_queen.png")
white_queen = pg.transform.scale(white_queen_load, (100, 100))

white_rook_load = pg.image.load(r"assets/White/w_rook.png")
white_rook = pg.transform.scale(white_rook_load, (100, 100))

white_knight_load = pg.image.load(r"assets/White/w_knight.png")
white_knight = pg.transform.scale(white_knight_load, (100, 100))

white_bishop_load = pg.image.load(r"assets/White/w_bishop.png")
white_bishop = pg.transform.scale(white_bishop_load, (100, 100))

white_pawn_load = pg.image.load(r"assets/White/w_pawn.png")
white_pawn = pg.transform.scale(white_pawn_load, (100, 100))
white_images = {
    "King": white_king,
    "Queen": white_queen,
    "Rook": white_rook,
    "Bishop": white_bishop,
    "Knight": white_knight,
    "Pawn": white_pawn,
}
black_images = {
    "King": black_king,
    "Queen": black_queen,
    "Rook": black_rook,
    "Bishop": black_bishop,
    "Knight": black_knight,
    "Pawn": black_pawn,
}


def draw_board():
    for i in range(32):
        file = i % 4
        rank = i // 4
        pg.draw.rect(
            window,
            "light gray",
            [(600 if rank % 2 == 0 else 700) - (file * 200), rank * 100, 100, 100],
        )
    for i in range(1, 8):
        pg.draw.line(window, "gold", (0, 100 * i), (800, 100 * i), 1)
        pg.draw.line(window, "gold", (100 * i, 0), (100 * i, 800), 1)


def draw_pieces():
    for coordinate, piece in white_pieces.items():
        file, rank = coordinate
        window.blit(white_images.get(piece), (file * 100, rank * 100))
    for coordinate, piece in black_pieces.items():
        file, rank = coordinate
        window.blit(black_images.get(piece), (file * 100, rank * 100))


run = True
while run:
    timer.tick(fps)
    window.fill("black")
    draw_board()
    draw_pieces()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()
pg.quit()
