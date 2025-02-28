import pygame
from game.world import World
from game.player import Player

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize world and player
        self.tile_size = 32
        self.world = World(self.width, self.height, self.tile_size)
        
        # Place player at the bottom center of the screen
        start_x = self.world.grid_width // 2
        start_y = self.world.grid_height - 2  # 2 tiles from bottom
        self.player = Player(start_x, start_y, self.world)
        
        # Camera position
        self.camera_x = 0
        self.camera_y = 0

    def update_camera(self):
        # Center the camera on the player
        target_camera_x = self.player.screen_x - self.width // 2
        target_camera_y = self.player.screen_y - self.height // 2
        
        # Smooth camera movement
        camera_speed = 0.1
        self.camera_x += (target_camera_x - self.camera_x) * camera_speed
        self.camera_y += (target_camera_y - self.camera_y) * camera_speed
        
        # Keep camera within bounds
        self.camera_x = max(0, min(self.camera_x, 
                                 self.world.grid_width * self.tile_size - self.width))
        self.camera_y = max(0, min(self.camera_y, 
                                 self.world.grid_height * self.tile_size - self.height))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "title"
        
        self.player.handle_action(event)
        return "game"

    def update(self):
        self.player.update()
        self.update_camera()

    def draw(self):
        # Clear screen
        self.screen.fill((100, 100, 100))
        
        # Draw world
        self.world.draw(self.screen, int(self.camera_x), int(self.camera_y))
        
        # Draw player
        self.player.draw(self.screen, int(self.camera_x), int(self.camera_y))
        
        # Draw UI elements here later
        
        pygame.display.flip() 