import pygame
import sys
import os

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=12)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Colors
        self.GREEN = (34, 139, 34)
        self.LIGHT_GREEN = (144, 238, 144)
        
        # Load background image if it exists
        self.background = None
        bg_path = os.path.join("assets", "images", "title_background.png")
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Create overlay surface for better text visibility
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.overlay, (255, 255, 255, 128), self.overlay.get_rect())
        
        # Create start button
        button_width = 200
        button_height = 60
        button_x = (self.width - button_width) // 2
        button_y = self.height * 0.7
        self.start_button = Button(
            button_x, button_y,
            button_width, button_height,
            "Start", self.GREEN, self.LIGHT_GREEN
        )
        
        # Title text
        self.title_font = pygame.font.Font(None, 100)
        self.title_text = self.title_font.render("Plant Daddy", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(
            center=(self.width // 2, self.height * 0.3)
        )

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback background
            self.screen.fill((200, 230, 200))
        
        # Add semi-transparent overlay
        self.screen.blit(self.overlay, (0, 0))
        
        # Draw title with shadow effect
        shadow_offset = 3
        shadow_text = self.title_font.render("Plant Daddy", True, (0, 0, 0))
        shadow_rect = self.title_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.screen.blit(shadow_text, shadow_rect)
        
        # Draw title
        self.screen.blit(self.title_text, self.title_rect)
        
        # Draw start button
        self.start_button.draw(self.screen)

    def handle_event(self, event):
        if self.start_button.handle_event(event):
            return "game"  # Transition to game state
        return "title"  # Stay on title screen 