from .board import Board
from .player import Player
import pygame
pygame.init()
import numpy as np

class Isolation:
    def __init__(self, width, height, window, visuals=True, window_width=800, window_height=800):
        self.board = Board(width, height)
        self.player1 = Player('Owen', 1, None)
        self.player2 = Player('Harry', 2, None)
        self.turn = 0
        
        # pygame setup
        if visuals:
            self.window = window
            self.window_width = window_width
            self.window_height = window_height
            self.cell_width = self.window_width // width
            self.cell_height = self.window_height // height
            
    def get_info(self):
        # open
        oCords = []
        # closed
        cCords = []
        
        # Iterate over the grid and collect coordinates
        for i in range(9):
            for j in range(9):
                value = self.board.grid[i, j]
                if value == 0:
                    oCords.append((i, j))
                elif value == 3:
                    coordinates_3.append((i, j))

        # Convert lists to NumPy arrays and flatten them
        oCords = np.array(oCords).flatten()
        cCords= np.array(cCords).flatten()
        
        return oCords, cCords, np.array(player1.pos), np.array(player2.pos)
    
    
    
    def draw_board(self):
        # Define colors
        COLORS = {
            0: (255, 255, 255),  # White for unoccupied
            1: (173, 216, 230),  # Light Blue for player 1
            2: (255, 192, 203),  # Pink for player 2
            3: (0, 0, 0)         # Black for walls (unchanged)
        }
        
        GRID_COLOR = (128, 128, 128)  # Gray for grid lines
        
        # Grid size
        grid_size = 9
        
        # Set up font for rendering text
        font = pygame.font.SysFont("Exo 2 Black", 36)  # You can adjust the font size as needed
        
        # Draw the board
        for y in range(grid_size):
            for x in range(grid_size):
                cell_value = self.board.grid[y, x]
                
                # Adjust the width and height of the last cell in the row/column
                current_cell_width = self.cell_width if x < grid_size - 1 else self.window_width - x * self.cell_width
                current_cell_height = self.cell_height if y < grid_size - 1 else self.window_height - y * self.cell_height
                
                # Draw the cell
                pygame.draw.rect(self.window, COLORS[cell_value],
                                pygame.Rect(x * self.cell_width, y * self.cell_height, current_cell_width, current_cell_height))
                
                
                # Draw the text "P1" or "P2" in the center of the cell if it's occupied by a player
                if cell_value == 1:
                    text = font.render("P1", True, (0, 0, 0))  # Black text for "P1"
                elif cell_value == 2:
                    text = font.render("P2", True, (0, 0, 0))  # Black text for "P2"
                else:
                    text = None
                
                if text:
                    text_rect = text.get_rect(center=(x * self.cell_width + current_cell_width // 2,
                                                    y * self.cell_height + current_cell_height // 2))
                    self.window.blit(text, text_rect)
                    
        # Draw grid lines
        for x in range(grid_size):
            pygame.draw.line(self.window, GRID_COLOR, (x * self.cell_width, 0), (x * self.cell_width, self.window_height))
        for y in range(grid_size):
            pygame.draw.line(self.window, GRID_COLOR, (0, y * self.cell_height), (self.window_width, y * self.cell_height))

        pygame.display.flip()  # Update the display

    def win_text(self, window, winner):
        font = pygame.font.SysFont("Exo 2 Black", 72) 
        victory_text = f"{winner} Wins!"
        text_surface = font.render(victory_text, True, (128, 0, 128))  # White text color
        text_rect = text_surface.get_rect(center=(self.window_width // 2, self.window_height // 2))
        window.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing or restarting


    def play(self, player1, player2):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
        clock = pygame.time.Clock()
        run = True
        self.draw_board()
        players = (self.player1, self.player2)
        
        while run:
            clock.tick(20)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row, col = mouse_y // self.cell_height, mouse_x // self.cell_width
                    
                    if self.board.move(players[self.turn], (row, col)):
                        # change turn to next player after successful move
                        self.turn = 1 if self.turn == 0 else 0
                        
                        # redraw new board with move on it
                        self.draw_board()
                        
                        # check if second player has any moves
                        if self.check_winner(players[self.turn]):
                            self.turn = 1 if self.turn == 0 else 0
                            self.win_text(self.window, players[self.turn].name)
                            run = False
                            break
                        
                    else:
                        print(f"Invalid Move By Player {self.turn+1} \nTo: {row},{col} \nFrom: {self.turn+1}")

            
            pygame.display.update()

        return self.turn
    
    def check_winner(self, player, valid_moves=None):
        # return -1 if Player 1 wins return 1 if Player 2 wins
        vMoves = valid_moves if valid_moves else self.board.get_moves(player)
        
        if player.pos and len(vMoves) == 0:
            return True
        
        return False

if __name__ == "__main__":
    width, height = 800, 800
    window = pygame.display.set_mode((width, height))
    
    iso = Isolation(9, 9, window, True, width, height)
    print(f'Player {iso.play("human","human")+1} Won')