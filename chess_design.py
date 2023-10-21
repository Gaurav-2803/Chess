# Inbuilt
import itertools

# Third Party
import pygame as p

# Project
import chess_main

HEIGHT = 784
WIDTH = 1000
DIMENSION = 8
PADDING = 8
BOARD_WIDTH = BOARD_HEIGHT = HEIGHT - (2 * PADDING)
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

BACKGROUND_COLOR = p.Color("#312e2b")
STATS_BOARD_COLOR = p.Color("#000000")
TEXT_COLOR = p.Color("#000000")
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
    FONT_SIZE = 15
    FONT = p.font.SysFont("freesansbold", FONT_SIZE)
    new_radius = 4
    for rank, file in itertools.product(range(DIMENSION), range(DIMENSION)):
        # Box
        box = (
            p.Rect(
                (file * SQUARE_SIZE) + PADDING,
                (rank * SQUARE_SIZE) + PADDING,
                SQUARE_SIZE,
                SQUARE_SIZE,
            ),
        )

        # Border Radius
        top_left_radius = (
            top_right_radius
        ) = bottom_left_radius = bottom_right_radius = -1
        if rank == 0:
            if file == 0:
                top_left_radius = new_radius
            elif file == 7:
                top_right_radius = new_radius
        elif rank == 7:
            if file == 0:
                bottom_left_radius = new_radius
            elif file == 7:
                bottom_right_radius = new_radius

        # Draw board
        color = colors[((rank + file) % 2)]
        p.draw.rect(
            screen,
            color,
            box,
            border_top_left_radius=top_left_radius,
            border_top_right_radius=top_right_radius,
            border_bottom_left_radius=bottom_left_radius,
            border_bottom_right_radius=bottom_right_radius,
        )

        # Draw Pieces
        piece = board[rank][file]
        if piece != "--":
            screen.blit(IMAGES.get(piece), box)

        # Draw Ranks Name
        if rank == 7:
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            txt = FONT.render(letters[file], True, TEXT_COLOR)
            screen.blit(
                txt,
                (
                    (file * SQUARE_SIZE) + SQUARE_SIZE / 2 + PADDING,
                    (rank * SQUARE_SIZE) + SQUARE_SIZE - (FONT_SIZE / 15),
                ),
            )

        # Draw Files Name
        if file == 0:
            nums = list(map(str, range(8, 0, -1)))
            txt = FONT.render(nums[rank], True, TEXT_COLOR)
            screen.blit(
                txt,
                (
                    (file * SQUARE_SIZE) + PADDING + (FONT_SIZE / 15),
                    (rank * SQUARE_SIZE) + SQUARE_SIZE / 2,
                ),
            )
    p.draw.rect(
        screen,
        STATS_BOARD_COLOR,
        p.Rect(
            BOARD_WIDTH + 2 * PADDING,
            PADDING,
            WIDTH - BOARD_WIDTH - 3 * PADDING,
            BOARD_HEIGHT,
        ),
        border_radius=new_radius,
    )


def main():
    # Intializing
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(BACKGROUND_COLOR)

    # Making chess board
    game_state = chess_main.GameState()
    load_images()
    draw_board(screen, game_state.board)

    # Running Game
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                square_clicked = tuple(map(lambda x: x // SQUARE_SIZE, event.pos))
                print(square_clicked)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
