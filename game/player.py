import pygame
from game.ui import Tool

class Player:
    def __init__(self, x, y, world):
        self.grid_x = x
        self.grid_y = y
        self.world = world
        self.move_speed = 5  # Grid cells per second
        self.last_move = 0
        self.move_cooldown = 200  # milliseconds
        
        # Movement animation
        self.screen_x = x * world.tile_size
        self.screen_y = y * world.tile_size
        self.target_x = self.screen_x
        self.target_y = self.screen_y
        
        # Player appearance
        self.color = (255, 0, 0)  # Red for now, will be replaced with sprite
        self.size = int(world.tile_size * 0.8)  # Slightly smaller than tile
        
        # Tools and interaction
        self.facing = 'down'  # down, up, left, right
        self.active_tool = Tool.HOE

    def update(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        # Only allow movement if we've reached our target position
        if self.screen_x == self.target_x and self.screen_y == self.target_y:
            if current_time - self.last_move >= self.move_cooldown:
                new_x, new_y = self.grid_x, self.grid_y
                
                # Handle movement input
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    new_x -= 1
                    self.facing = 'left'
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    new_x += 1
                    self.facing = 'right'
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    new_y -= 1
                    self.facing = 'up'
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    new_y += 1
                    self.facing = 'down'
                
                # Check if the new position is valid
                if self.world.is_walkable(new_x, new_y):
                    self.grid_x, self.grid_y = new_x, new_y
                    self.target_x = new_x * self.world.tile_size
                    self.target_y = new_y * self.world.tile_size
                    self.last_move = current_time
        
        # Smooth movement animation
        move_speed = 5
        if self.screen_x < self.target_x:
            self.screen_x = min(self.screen_x + move_speed, self.target_x)
        elif self.screen_x > self.target_x:
            self.screen_x = max(self.screen_x - move_speed, self.target_x)
            
        if self.screen_y < self.target_y:
            self.screen_y = min(self.screen_y + move_speed, self.target_y)
        elif self.screen_y > self.target_y:
            self.screen_y = max(self.screen_y - move_speed, self.target_y)

    def set_active_tool(self, tool):
        self.active_tool = tool

    def handle_action(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.interact()

    def interact(self):
        # Get the tile in front of the player
        target_x, target_y = self.grid_x, self.grid_y
        
        if self.facing == 'up':
            target_y -= 1
        elif self.facing == 'down':
            target_y += 1
        elif self.facing == 'left':
            target_x -= 1
        elif self.facing == 'right':
            target_x += 1
            
        tile = self.world.get_tile(target_x, target_y)
        
        # Use the active tool
        if self.active_tool == Tool.HOE and tile == self.world.Tile.SOIL:
            self.world.set_tile(target_x, target_y, self.world.Tile.TILLED_SOIL)
        elif self.active_tool == Tool.WATER and tile == self.world.Tile.TILLED_SOIL:
            self.world.set_tile(target_x, target_y, self.world.Tile.WATERED_SOIL)
        # Add more tool interactions here later

    def draw(self, screen, camera_x=0, camera_y=0):
        # Draw the player as a circle for now
        center_x = self.screen_x + self.world.tile_size // 2 - camera_x
        center_y = self.screen_y + self.world.tile_size // 2 - camera_y
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.size // 2)
        
        # Draw a small line indicating facing direction
        direction_length = 10
        if self.facing == 'up':
            end_y = center_y - direction_length
            end_x = center_x
        elif self.facing == 'down':
            end_y = center_y + direction_length
            end_x = center_x
        elif self.facing == 'left':
            end_x = center_x - direction_length
            end_y = center_y
        else:  # right
            end_x = center_x + direction_length
            end_y = center_y
            
        pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (end_x, end_y), 2) 