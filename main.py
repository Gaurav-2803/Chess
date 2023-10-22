# Inbuilt
import itertools

# Third Party
import pygame as p

# Project
from resources.styles.brown import *
from src import moves, state

HEIGHT = 784
WIDTH = 1000
DIMENSION = 8
PADDING = 12
BOARD_WIDTH = BOARD_HEIGHT = HEIGHT - (2 * PADDING)
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"resources/pieces/black_white/{piece}.png"),
            (SQUARE_SIZE, SQUARE_SIZE),
        )


def draw_board(screen, game_state):
    colors = [LIGHT_BOX_COLOR, DARK_BOX_COLOR]
    # FONT_SIZE = 25
    # FONT = p.font.SysFont("freesans", FONT_SIZE)
    new_radius = 4
    for row, col in itertools.product(range(DIMENSION), range(DIMENSION)):
        # Box
        box = (
            p.Rect(
                (col * SQUARE_SIZE) + PADDING,
                (row * SQUARE_SIZE) + PADDING,
                SQUARE_SIZE,
                SQUARE_SIZE,
            ),
        )

        # Border Radius
        top_left_radius = (
            top_right_radius
        ) = bottom_left_radius = bottom_right_radius = -1
        if row == 0 and col == 0:
            top_left_radius = new_radius
        elif row == 0 and col == 7:
            top_right_radius = new_radius
        elif row == 7 and col == 0:
            bottom_left_radius = new_radius
        elif row == 7 and col == 7:
            bottom_right_radius = new_radius

        # Draw board
        color = colors[((row + col) % 2)]
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
        piece = game_state.board[row][col]
        if piece != "--":
            screen.blit(IMAGES.get(piece), box)

        # # Draw Ranks Name
        # if row == 7:
        #     letters = [chr(97 + x) for x in range(8)]
        #     txt = FONT.render(letters[col], True, TEXT_COLOR)
        #     screen.blit(
        #         txt,
        #         (
        #             (col * SQUARE_SIZE) + SQUARE_SIZE / 2 + PADDING,
        #             HEIGHT - PADDING,
        #         ),
        #     )

        # # Draw Files Name
        # if col == 0:
        #     nums = list(map(str, range(8, 0, -1)))
        #     txt = FONT.render(nums[row], True, TEXT_COLOR)
        #     screen.blit(
        #         txt,
        #         (
        #             (col * SQUARE_SIZE) + PADDING + (FONT_SIZE / 15),
        #             (row * SQUARE_SIZE) + SQUARE_SIZE / 2,
        #         ),
        #     )
    # Draw Stats Board
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
    game_state = state.GameState()

    # All Valid moves
    valid_moves = game_state.get_valid_moves()
    move_made = False

    load_images()
    # Keeping Track of moves
    selected_square = ()
    player_clicked = []
    # Running Game
    running = True
    while running:
        for event in p.event.get():
            # Quit
            if event.type == p.QUIT:
                running = False
            # Make Move
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                # Fetch Mouse Click Position
                col, row = tuple(map(lambda x: (x - PADDING) // SQUARE_SIZE, event.pos))
                # Check if poisition already pressed or not
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicked = []
                else:
                    selected_square = (row, col)
                    player_clicked.append(selected_square)
                # If two different valid position, move the piece
                if len(player_clicked) == 2:
                    move = moves.Move(
                        player_clicked[0], player_clicked[1], game_state.board
                    )
                    move.get_chess_notation()

                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                        selected_square = ()
                        player_clicked = []
                    else:
                        player_clicked = [selected_square]

            # Undo Move
            elif event.type == p.KEYDOWN and event.key == p.K_z:
                game_state.undo_move()
                move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_board(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
