import pygame
from game.world import World
from game.player import Player
from game.ui import ToolBar, StatusPanel

class GameScreen:
    def __init__(self, screen):
        """Initialize the game screen with all necessary components"""
        if not isinstance(screen, pygame.Surface):
            raise TypeError("screen must be a pygame.Surface")
            
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize world and player
        self.tile_size = 32
        self.world = World(self.width, self.height, self.tile_size)
        
        # Place player at the bottom center of the screen in pixel coordinates
        start_x = (self.world.grid_width // 2) * self.tile_size
        start_y = (self.world.grid_height - 2) * self.tile_size  # 2 tiles from bottom
        self.player = Player(start_x, start_y, self.world)
        
        # Camera position (in pixels)
        self.camera_x = 0
        self.camera_y = 0
        
        # UI elements
        self.toolbar = ToolBar(self.width, self.height)
        self.status_panel = StatusPanel(self.width)
        
        # Game clock for time tracking
        self.last_update = pygame.time.get_ticks()
        
        # Debug mode
        self.debug = False

    def update_camera(self):
        """Update camera position to follow the player with smooth movement"""
        try:
            # Center the camera on the player (using pixel coordinates)
            target_camera_x = self.player.x - self.width // 2
            target_camera_y = self.player.y - self.height // 2
            
            # Smooth camera movement
            camera_speed = 0.1
            self.camera_x += (target_camera_x - self.camera_x) * camera_speed
            self.camera_y += (target_camera_y - self.camera_y) * camera_speed
            
            # Calculate world bounds in pixels
            max_camera_x = self.world.grid_width * self.tile_size - self.width
            max_camera_y = self.world.grid_height * self.tile_size - self.height
            
            # Keep camera within bounds
            self.camera_x = max(0, min(self.camera_x, max_camera_x))
            self.camera_y = max(0, min(self.camera_y, max_camera_y))
            
        except AttributeError as e:
            print(f"Camera update error: {e}")
            # Fallback to center if there's an error
            self.camera_x = max(0, min(self.player.x - self.width // 2, max_camera_x))
            self.camera_y = max(0, min(self.player.y - self.height // 2, max_camera_y))

    def handle_event(self, event):
        """Handle all game events including debug commands"""
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "title"
                elif event.key == pygame.K_F3:  # Toggle debug mode
                    self.debug = not self.debug
            
            # Handle toolbar events
            if self.toolbar.handle_event(event):
                self.player.selected_tool = self.toolbar.get_selected_tool()
            
            # Handle player action (space key for using tools)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.use_tool()
                
        except Exception as e:
            print(f"Event handling error: {e}")
            
        return "game"

    def update(self):
        """Update game state including player, camera, and UI"""
        try:
            current_time = pygame.time.get_ticks()
            dt = current_time - self.last_update
            self.last_update = current_time
            
            # Get keyboard state
            keys = pygame.key.get_pressed()
            
            # Update components
            self.player.update(dt, keys)
            self.update_camera()
            self.status_panel.update(dt)
            
        except Exception as e:
            print(f"Update error: {e}")

    def draw(self):
        """Draw all game elements including debug information if enabled"""
        try:
            # Clear screen
            self.screen.fill((100, 100, 100))
            
            # Draw world
            self.world.draw(self.screen, int(self.camera_x), int(self.camera_y))
            
            # Draw player
            self.player.draw(self.screen, int(self.camera_x), int(self.camera_y))
            
            # Draw UI elements
            self.toolbar.draw(self.screen)
            self.status_panel.draw(self.screen)
            
            # Draw debug information
            if self.debug:
                debug_font = pygame.font.Font(None, 24)
                debug_info = [
                    f"FPS: {int(1000 / max(1, pygame.time.get_ticks() - self.last_update))}",
                    f"Player Pos: ({int(self.player.x)}, {int(self.player.y)})",
                    f"Camera Pos: ({int(self.camera_x)}, {int(self.camera_y)})",
                    f"Selected Tool: {self.player.selected_tool}"
                ]
                
                for i, text in enumerate(debug_info):
                    surface = debug_font.render(text, True, (255, 255, 255))
                    self.screen.blit(surface, (10, self.height - 100 + i * 20))
            
            pygame.display.flip()
            
        except Exception as e:
            print(f"Draw error: {e}")
            # Attempt to recover by flipping the display
            pygame.display.flip() 