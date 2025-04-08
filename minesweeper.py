import numpy as np
import pygame
from config import BUTTON_HEIGHT, BLUE, BLACK, WHITE, TILE_SIZE, MARGIN

border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("sprites/empty.png")
spr_flag = pygame.image.load("sprites/flag.png")
spr_grid = pygame.image.load("sprites/Grid.png")
spr_grid1 = pygame.image.load("sprites/grid1.png")
spr_grid2 = pygame.image.load("sprites/grid2.png")
spr_grid3 = pygame.image.load("sprites/grid3.png")
spr_grid4 = pygame.image.load("sprites/grid4.png")
spr_grid5 = pygame.image.load("sprites/grid5.png")
spr_grid6 = pygame.image.load("sprites/grid6.png")
spr_grid7 = pygame.image.load("sprites/grid7.png")
spr_grid8 = pygame.image.load("sprites/grid8.png")
spr_grid7 = pygame.image.load("sprites/grid7.png")
spr_mine = pygame.image.load("sprites/mine.png")

class GameBoard:
    """Generate the board for the game"""
    def __init__(
        self,
        screen,
        board_width: int = 9,
        board_height: int = 10,
        mines_number: int = 10,
        game_level: int = None,
    ):

        self.board_height = board_height
        self.board_width = board_width
        self.mines_number = mines_number

        # set default state to 9: empty cell
        self.game_state = 9 * np.ones([self.board_height, self.board_width])
        self.mask_reveal = np.zeros([self.board_height, self.board_width])
        self.mines_pos = np.zeros([self.board_height, self.board_width])

        self.lock_button = False
        self.screen = screen
        
        self.window_width = MARGIN + board_width * (TILE_SIZE + MARGIN)
        self.window_height = MARGIN + board_height * (TILE_SIZE + MARGIN) + BUTTON_HEIGHT * 2

        self.text_state = ""
        
        # Generating entire grid
        if screen != None:
            self.grids = []
            for row in range(board_height):
                line = []
                for col in range(board_width):
                    x = MARGIN + col * (TILE_SIZE + MARGIN)
                    y = MARGIN + row * (TILE_SIZE + MARGIN)
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    line.append(Grid(col, row, self.mines_pos[row,col], rect, screen))
                self.grids.append(line)

            self.update_ui_state()

    def get_adjacent_cells(self, board, point):
        r, c = point
        rlb, rub = np.clip(r-1, 0, self.board_height), np.clip(r+2, 0, self.board_height)
        clb, cub = np.clip(c-1, 0, self.board_width), np.clip(c+2, 0, self.board_width)
        return board[rlb:rub, clb:cub]

    def set_adjacent_cells(self, board, point, value):
        r, c = point
        rlb, rub = np.clip(r-1, 0, self.board_height), np.clip(r+2, 0, self.board_height)
        clb, cub = np.clip(c-1, 0, self.board_width), np.clip(c+2, 0, self.board_width)
        board[rlb:rub, clb:cub] = value
        return board

    def helper_number(self):
        numb_info = np.zeros([self.board_height, self.board_width])
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.mines_pos[i, j]==1:
                    numb_info[i,j] = -1
                    continue
                range_pos = self.get_adjacent_cells(self.mines_pos, (i,j))
                numb_info[i,j] = np.sum(range_pos)
                if np.sum(range_pos)==0:
                    numb_info[i,j] = 9
        return numb_info

    def generate(self, first_clicked_point):
        self.mines_pos = np.zeros([self.board_height, self.board_width])

        # Mask the adjacent cells around the first clicked cell that should not contain mines (safe zone)
        self.mines_pos = self.set_adjacent_cells(self.mines_pos, first_clicked_point, 1)
        
        # Get index of cells outside from the safe zone
        mines_zone = np.argwhere(self.mines_pos==0)

        # Randomly define the mine position
        idx = np.random.choice(len(mines_zone), size=self.mines_number, replace=False)
        for r, c in mines_zone[idx]:
            self.mines_pos[r,c] = 1

        # Remove the safe zone mask
        self.mines_pos = self.set_adjacent_cells(self.mines_pos, first_clicked_point, 0)

        self.game_state = self.helper_number()

        if self.screen != None:
            self.update_ui_state()

        return self.mines_pos
    
    def check_win_status(self):
        # Check if the unrevealed cell number is the same with the mine number
        pred_mines = self.board_height * self.board_width - np.sum(self.mask_reveal)
        if pred_mines == np.sum(self.mines_pos):
            self.lock_button = True
            self.text_state = "You win!"

    def update_ui_state(self):
        states = self.mask_reveal * self.game_state
        drawText(self.screen, self.text_state, self.window_height, self.window_width) 
        for row in range(len(self.grids)):
            for col in range(len(self.grids[0])):
                self.grids[row][col].val = states[row][col]
                self.grids[row][col].drawGrid()
    
    def reveal(self, clicked_point):
        r, c = clicked_point
        rlb, rub = np.clip(r-1, 0, self.board_height-1), np.clip(r+2, 0, self.board_height-1)
        clb, cub = np.clip(c-1, 0, self.board_width-1), np.clip(c+2, 0, self.board_width-1)
        adjacent_cells = self.get_adjacent_cells(self.game_state, clicked_point)

        mask = self.get_adjacent_cells(self.mask_reveal, clicked_point)
        mask[adjacent_cells!=-1] = 1
        
        for i in range(rlb, rub+1, 1):
            for j in range(clb, cub+1, 1):
                if self.game_state[i,j] != 9:
                    continue
                adjacent_cells = self.get_adjacent_cells(self.game_state, (i,j))
                mask = self.get_adjacent_cells(self.mask_reveal, (i,j))
                filter = adjacent_cells[mask!=1]
                filter = filter[filter!=-1]
                if len(filter)>0:
                    self.reveal((i,j))

    def reveal_all_mines(self):
        self.mask_reveal += self.mines_pos
        self.lock_button = True
        self.text_state = "Don't give up!"

    def leftClick_cell(self, row, col):
        # Only reveal a cell if there is no flag on it
        if not self.grids[row][col].flag and not self.lock_button:
            # Check if the cell contain mines
            if self.mines_pos[row][col] == 1:
                self.reveal_all_mines()

            # Check if the cell empty
            elif self.game_state[row][col] != 9:
                self.mask_reveal[row][col] = 1

            else:
                self.reveal((row,col))

    def rightClick_cell(self, row, col):
        # Flag a cell
        if (self.mask_reveal[row][col] == 0 or self.grids[row][col].flag) and not self.lock_button:
            self.grids[row][col].flag = not self.grids[row][col].flag
            self.mask_reveal[row][col] = 0


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type, rect, screen):
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.flag = False  # Bool var to check if player flagged the grid
        self.rect = rect
        self.val = type  # Value of the grid, -1 is mine
        self.screen = screen

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        # Mine
        if self.flag:
            self.screen.blit(spr_flag, self.rect)
        else:
            if self.val == -1: 
                self.screen.blit(spr_mine, self.rect)
            # Unclicked cell
            elif self.val == 0: 
                self.screen.blit(spr_grid, self.rect)
            # 1 adjacent mine
            elif self.val == 1: 
                self.screen.blit(spr_grid1, self.rect)
            # 2 adjacent mines
            elif self.val == 2: 
                self.screen.blit(spr_grid2, self.rect)
            # 3 adjacent mines
            elif self.val == 3: 
                self.screen.blit(spr_grid3, self.rect)
            # 4 adjacent mines
            elif self.val == 4: 
                self.screen.blit(spr_grid4, self.rect)
            # 5 adjacent mines
            elif self.val == 5: 
                self.screen.blit(spr_grid5, self.rect)
            # 6 adjacent mines
            elif self.val == 6: 
                self.screen.blit(spr_grid6, self.rect)
            # 7 adjacent mines
            elif self.val == 7: 
                self.screen.blit(spr_grid7, self.rect)
            # 8 adjacent mines
            elif self.val == 8: 
                self.screen.blit(spr_grid8, self.rect)
            # empty cell
            elif self.val == 9: 
                self.screen.blit(spr_emptyGrid, self.rect)


def draw_button(screen, font, window_height, window_width):
    button_rect = pygame.Rect(MARGIN, window_height - BUTTON_HEIGHT - MARGIN, 
                              window_width - 2 * MARGIN, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLUE, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    label = font.render("New Game", True, WHITE)
    screen.blit(label, (button_rect.centerx - label.get_width() // 2, 
                        button_rect.centery - label.get_height() // 2))
    return button_rect


def drawText(screen, text, window_height, window_width):
    font = pygame.font.SysFont(None, 36)
    button_rect = pygame.Rect(MARGIN, window_height - BUTTON_HEIGHT * 2 - MARGIN, 
                              window_width - 2 * MARGIN, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLACK, button_rect)
    # pygame.draw.rect(screen, BLACK, button_rect, 2)
    label = font.render(text, True, WHITE)
    screen.blit(label, (button_rect.centerx - label.get_width() // 2, 
                        button_rect.centery - label.get_height() // 2))