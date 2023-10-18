import itertools

import pygame as p

import chess_main

WIDTH = HEIGHT = 768
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"assets/theme_1/pieces_img/{piece}.png"),
            (SQUARE_SIZE, SQUARE_SIZE),
        )


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
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


def draw_board(screen):
    colors = [p.Color("#f1d9b5"), p.Color("#b58863")]
    for rank, file in itertools.product(range(DIMENSION), range(DIMENSION)):
        color = colors[((rank + file) % 2)]
        p.draw.rect(
            screen,
            color,
            p.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        )


def draw_pieces(screen, board):
    pass


def draw_game_state(screen, game_state):
    draw_board(screen)


if __name__ == "__main__":
    main()
