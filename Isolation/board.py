import numpy as np


class Board:
    
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        
        # 0-unoccupied      1-player 1      2-player 2      3-wall
        # Instantiate unoccupied grid
        self.grid = self.init_grid(width, height)
        
    def __str__(self):
        # Define a mapping for the grid values to symbols
        symbols = {0: '.', 1: 'P1', 2: 'P2', 3: '█'}
        
        # Determine the maximum width of the symbols to align the grid
        symbol_width = max(len(symbols[cell]) for cell in self.grid.flat)
        
        top = ' ' + ' '.join(['_' * (symbol_width + 1) for _ in range(self.width-1)])
        bottom = ' ' + ' '.join(['⎻' * (symbol_width + 1) for _ in range(self.width-1)])
        
        
        grid_str = "------------Board------------\n"
        
        grid_str += top + '\n'
        
        for row in self.grid:
            row_str = ' '.join(f'{symbols[cell]:<{symbol_width}}' for cell in row)
            grid_str += f'| {row_str} |\n'
        
        grid_str += bottom
        
        return grid_str
    
    def get_info(self):
        # open
        oCords = []
        # closed
        cCords = []
        
        # Iterate over the grid and collect coordinates
        for i in range(9):
            for j in range(9):
                value = self.grid[i, j]
                if value == 0:
                    oCords.append((i, j))
                elif value == 3:
                    coordinates_3.append((i, j))

        # Convert lists to NumPy arrays and flatten them
        oCords = np.array(oCords).flatten()
        cCords= np.array(cCords).flatten()
        
        return oCords, cCords
    
    def init_grid(self, width, height):
        grid = np.full((height, width), 0, dtype=np.uint8)
        
        
        grid[2,2:4] = 3
        grid[3,2] = 3
        
        grid[2,5:7] = 3
        grid[3,6] = 3
        
        grid[6,2:4] = 3
        grid[5,2] = 3
        grid[6,5:7] = 3
        grid[5,6] = 3
        
        return grid       
        
    def get_moves(self, player):
        moves = set()
        
        if player.pos:
            directions = [
                (-1, 0), (1, 0),  # Vertical
                (0, -1), (0, 1),  # Horizontal
                (-1, -1), (-1, 1),  # Diagonals
                (1, -1), (1, 1)
            ]

            
            row, col = player.pos
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Check if the new position is within bounds and unoccupied
                while (0 <= new_row < self.height and 0 <= new_col < self.width and self.grid[new_row, new_col] == 0):
                    moves.add((new_row, new_col))
                    new_row, new_col = new_row + dr, new_col + dc
        else:
            for i in range(9):
                for j in range(9):
                    value = self.grid[i, j]
                    if value == 0:
                        moves.add((i, j))
        
        return moves

    # move - (row, col)
    def move(self, player, move, valid_moves = None):
        
        if not valid_moves:
            valid_moves = self.get_moves(player)
    
        if move in valid_moves:
            if player.pos:
                self.grid[player.pos] = 3
                
            # print(move)
            self.grid[move] = player.number
            player.pos = move
            player.moves += 1
            
            return True
        
        
        
        return False
        
        
    
if __name__ == "__main__":
    grid = Board(9,9)
    print(grid)



