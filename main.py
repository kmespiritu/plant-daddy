import pygame
import sys
from screens.title_screen import TitleScreen

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Plant Daddy")
clock = pygame.time.Clock()

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.state = "title"
        self.title_screen = TitleScreen(screen)

    def run(self):
        while True:
            if self.state == "title":
                self.run_title_screen()
            elif self.state == "game":
                self.run_game()

    def run_title_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # Handle title screen events
            self.state = self.title_screen.handle_event(event)

        # Draw title screen
        self.title_screen.draw()
        pygame.display.flip()
        clock.tick(60)

    def run_game(self):
        # Clear the screen
        screen.fill(GREEN)
        
        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "title"
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)

def main():
    game_state = GameState(screen)
    game_state.run()

if __name__ == "__main__":
    main() 