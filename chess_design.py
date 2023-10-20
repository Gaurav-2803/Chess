# Inbuilt
import itertools

# Third Party
import pygame as p

# Project
import chess_main

HEIGHT = 800
WIDTH = 1000
BOARD_WIDTH = 800
DIMENSION = 8
LEFT_PADDING = 24
TOP_PADDING = 8
SQUARE_SIZE = (BOARD_WIDTH - LEFT_PADDING - TOP_PADDING) // DIMENSION
MAX_FPS = 60
IMAGES = {}

BACKGROUND_COLOR = p.Color("#312e2b")
TEXT_COLOR = p.Color("#989695")
LIGHT_BOX_COLOR = p.Color("#f1d9b5")
DARK_BOX_COLOR = p.Color("#b58863")


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"assets/theme_1/pieces_img/{piece}.png"),
            (SQUARE_SIZE, SQUARE_SIZE),
        )


def draw_board(screen, board):
    colors = [LIGHT_BOX_COLOR, DARK_BOX_COLOR]
    FONT = p.font.SysFont("Times New Roman", 20)
    for rank, file in itertools.product(range(DIMENSION), range(DIMENSION)):
        # Box
        box = (
            p.Rect(
                (file * SQUARE_SIZE) + LEFT_PADDING,
                (rank * SQUARE_SIZE) + TOP_PADDING,
                SQUARE_SIZE,
                SQUARE_SIZE,
            ),
        )
        # Draw board
        color = colors[((rank + file) % 2)]
        p.draw.rect(screen, color, box)
        # Draw Pieces
        piece = board[rank][file]
        if piece != "--":
            screen.blit(IMAGES.get(piece), box)

        # Draw Ranks Name
        # if rank == 7:
        #     letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        #     txt = FONT.render(letters[rank], True, TEXT_COLOR)
        #     screen.blit(
        #         txt,
        #         p.Rect(
        #             ((file * SQUARE_SIZE) + LEFT_PADDING),
        #             776 + TOP_PADDING,
        #             SQUARE_SIZE,
        #             SQUARE_SIZE,
        #         ),
        #     )
        # Draw Files Name


def draw_index(screen):
    FONT = p.font.SysFont("Times New Roman", 20)
    start = LEFT_PADDING + (SQUARE_SIZE / 2) - DIMENSION
    increment = SQUARE_SIZE

    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        txt = FONT.render(letter, True, TEXT_COLOR)
        screen.blit(txt, (start, 776))
        start += increment

    start = TOP_PADDING + (SQUARE_SIZE / 2) - DIMENSION
    for num in range(8, 0, -1):
        txt = FONT.render(str(num), True, TEXT_COLOR)
        screen.blit(txt, (6, start))
        start += increment


def draw_game_state(screen, game_state):
    draw_board(screen, game_state.board)
    draw_index(screen)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(BACKGROUND_COLOR)
    game_state = chess_main.GameState()
    load_images()
    draw_game_state(screen, game_state)
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
