import pygame
import sys
import numpy as np
import re
from minesweeper import GameBoard, draw_button, drawText
from config import parse_args, MARGIN, TILE_SIZE, BUTTON_HEIGHT, BLACK


# --- Configuration ---
args = parse_args()

# Load variables from argparse
board_height = args.board_height
board_width = args.board_width
mines_number = args.mines_number
game_level = args.game_level
# Convert the game level
if game_level != None:
    game_level = str(game_level).lower()
    level_dict = {
        'easy': 1,
        'medium': 2,
        'hard': 3
    }
    game_level = level_dict[game_level]
    # Easy level
    if game_level==1:
        board_width = 9
        board_height = 10
        mines_number = 10

    # Medium level
    elif game_level==2:
        board_height = 15
        board_width = 13
        mines_number = 40

    # Hard level
    elif game_level==3:
        board_width = 16
        board_height = 30
        mines_number = 99

gui_enabled = args.gui

# Make sure mines_number not exceed the limit
limit = board_height * board_width - 9
if mines_number > limit:
    print(f"Mines exceeding limit! reset it to {limit-1}")
    mines_number = limit-1


# Print settings configuration
print()
print("----------------------")
print("CONFIGURATION")
print("----------------------")
print(f"  Board Height: {board_height}")
print(f"  Board Width: {board_width}")
print(f"  Mines: {mines_number}")
print(f"  Game Level: {game_level}")
print(f"  GUI Enabled: {gui_enabled}")
print()

window_width = MARGIN + board_width * (TILE_SIZE + MARGIN)
window_height = MARGIN + board_height * (TILE_SIZE + MARGIN) + BUTTON_HEIGHT * 2

# Setup screen
if gui_enabled:
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("MinesweeperzzZ")

    # Fonts
    font = pygame.font.SysFont(None, 36)

mines_pos = np.zeros([10, 9])

# --- Renew the game state ---
def new_game(
        screen,
        board_width: int = 9,
        board_height: int = 10,
        mines_number: int = 10
    ):

    global first_clicked
    global mines_pos
    global gameBoard
    first_clicked = False
    mines_pos = np.zeros([10, 9])
    gameBoard = GameBoard(
                    game_level=game_level,
                    board_width=board_width,
                    board_height=board_height,
                    mines_number=mines_number,
                    screen=screen
                )
    print("New game started!")

# def handle_tile_leftClick(row, col):
#     # Event trigger on left mouse click
#     gameBoard.leftClick_cell(row, col)
#     # print(f"Tile clicked: ({row}, {col}) | Value: {mines_pos[row][col]}")


def parse_coordinates(input_str):
    # Split the input by comma
    parts = str(input_str).split(',')

    # Check if there are exactly 2 parts
    if len(parts) != 2:
        print("Warning: Input must be two numbers separated by a comma, e.g., '10, 9'")
        return None

    coords = []
    for part in parts:
        # Remove non-numeric characters (except minus sign)
        cleaned = re.sub(r"[^\d\-]", "", part)
        if cleaned == '' or not re.match(r"^-?\d+$", cleaned):
            print(f"Warning: '{part}' is not a valid number.")
            return None
        coords.append(int(cleaned))

    x, y = coords
    if x-1 > board_width or y-1 > board_height or x-1 < 0 or y-1 < 0:
        print("Warning: Input position cannot exced the grid size")
        return None
    return x, y

# Initialize Pygame
# --- Main Loop ---
global first_clicked
# Running on GUI mode
if gui_enabled:
    new_game(
        screen=screen,
        board_width=board_width,
        board_height=board_height,
        mines_number=mines_number)
    running = True
    while running:
        screen.fill(BLACK)
        gameBoard.update_ui_state()
        button_rect = draw_button(screen, font, window_height, window_width)
        # drawText(screen, gameBoard.text_state, window_height, window_width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Left Mouse clicked
                if pygame.mouse.get_pressed()[0]:
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        new_game(
                            screen,
                            board_width=board_width,
                            board_height=board_height,
                            mines_number=mines_number)

                    # Check tile click
                    for row in range(board_height):
                        for col in range(board_width):
                            x = MARGIN + col * (TILE_SIZE + MARGIN)
                            y = MARGIN + row * (TILE_SIZE + MARGIN)
                            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                            # Tile is clicked
                            if rect.collidepoint(mouse_x, mouse_y):
                                if not first_clicked and not gameBoard.grids[row][col].flag:
                                    first_clicked = True
                                    print("Mines position defined!")
                                    mines_pos = gameBoard.generate((row, col))
                                gameBoard.leftClick_cell(row, col)
                                gameBoard.check_win_status()

                # Right Mouse clicked
                elif pygame.mouse.get_pressed()[2]:
                    for row in range(board_height):
                        for col in range(board_width):
                            x = MARGIN + col * (TILE_SIZE + MARGIN)
                            y = MARGIN + row * (TILE_SIZE + MARGIN)
                            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                            # Tile is clicked
                            if rect.collidepoint(mouse_x, mouse_y):
                                gameBoard.rightClick_cell(row, col)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Running on console mode (only able to generate the mines position)
else:
    new_game(
        screen=None,
        board_width=board_width,
        board_height=board_height,
        mines_number=mines_number)
    position=None
    n = 0
    while position==None:
        if n>5:
            # Exit the program if the input fail for 5 times
            sys.exit()
        position = input("Enter the first click position e.g. 10, 9 (row-n., column-n): ")
        position = parse_coordinates(position)
        n += 1
    row, col = parse_coordinates(position)
    mines_pos = gameBoard.generate((row, col))
    print(mines_pos)
    