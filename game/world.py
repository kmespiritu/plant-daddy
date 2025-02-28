import pygame
import numpy as np

class Tile:
    GRASS = 0
    SOIL = 1
    TILLED_SOIL = 2
    WATERED_SOIL = 3
    PATH = 4

    @staticmethod
    def get_color(tile_type):
        colors = {
            Tile.GRASS: (34, 139, 34),      # Green
            Tile.SOIL: (139, 69, 19),       # Brown
            Tile.TILLED_SOIL: (105, 53, 15), # Dark Brown
            Tile.WATERED_SOIL: (76, 38, 11), # Darker Brown
            Tile.PATH: (210, 180, 140)       # Light Brown
        }
        return colors.get(tile_type, (0, 0, 0))

class World:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid_width = width // tile_size
        self.grid_height = height // tile_size
        
        # Initialize the world grid with grass
        self.grid = np.full((self.grid_height, self.grid_width), Tile.GRASS, dtype=int)
        
        # Create a center garden plot
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        garden_size = 5
        
        # Create a garden plot with soil
        for y in range(center_y - garden_size, center_y + garden_size):
            for x in range(center_x - garden_size, center_x + garden_size):
                if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
                    self.grid[y, x] = Tile.SOIL
        
        # Add a path leading to the garden
        for y in range(center_y + garden_size, self.grid_height):
            if 0 <= y < self.grid_height:
                self.grid[y, center_x] = Tile.PATH

    def get_tile(self, grid_x, grid_y):
        if 0 <= grid_y < self.grid_height and 0 <= grid_x < self.grid_width:
            return self.grid[grid_y, grid_x]
        return None

    def set_tile(self, grid_x, grid_y, tile_type):
        if 0 <= grid_y < self.grid_height and 0 <= grid_x < self.grid_width:
            self.grid[grid_y, grid_x] = tile_type

    def screen_to_grid(self, screen_x, screen_y):
        grid_x = screen_x // self.tile_size
        grid_y = screen_y // self.tile_size
        return grid_x, grid_y

    def grid_to_screen(self, grid_x, grid_y):
        screen_x = grid_x * self.tile_size
        screen_y = grid_y * self.tile_size
        return screen_x, screen_y

    def draw(self, screen, camera_x=0, camera_y=0):
        # Draw each tile
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                # Only draw tiles that are visible on screen
                if (-self.tile_size <= screen_x <= self.width and 
                    -self.tile_size <= screen_y <= self.height):
                    tile_type = self.grid[y, x]
                    color = Tile.get_color(tile_type)
                    rect = pygame.Rect(screen_x, screen_y, self.tile_size - 1, self.tile_size - 1)
                    pygame.draw.rect(screen, color, rect)

    def is_walkable(self, grid_x, grid_y):
        tile = self.get_tile(grid_x, grid_y)
        return tile is not None  # For now, all tiles are walkable 