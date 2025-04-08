import argparse

TILE_SIZE = 30
MARGIN = 2
BUTTON_HEIGHT = 50

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

def parse_args():
    parser = argparse.ArgumentParser(description="Board Configuration Settings")
    
    parser.add_argument("--board_height", type=int, default=10, help="Height of the board (number of tiles)")
    parser.add_argument("--board_width", type=int, default=9, help="Width of the board (number of tiles)")
    parser.add_argument("--mines_number", type=int, default=9, help="Number of mines")
    parser.add_argument("--game_level", type=str, default=None, help="Difficulty level (easy, medium, hard)")
    parser.add_argument("--gui", action="store_true", help="Enable GUI mode")

    return parser.parse_args()