import pygame
import os

# Initialize Pygame
pygame.init()

# Icon size (32x32 pixels)
ICON_SIZE = 32

# Create output directory if it doesn't exist
os.makedirs(os.path.join("assets", "ui"), exist_ok=True)

def create_hoe_icon():
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    
    # Handle (brown)
    pygame.draw.rect(surface, (139, 69, 19), (14, 8, 4, 20))
    
    # Blade (gray)
    pygame.draw.rect(surface, (192, 192, 192), (8, 4, 16, 6))
    pygame.draw.rect(surface, (160, 160, 160), (8, 4, 4, 4))
    
    return surface

def create_water_icon():
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    
    # Watering can body (light blue)
    pygame.draw.rect(surface, (135, 206, 235), (8, 12, 16, 12))
    pygame.draw.rect(surface, (135, 206, 235), (20, 8, 8, 4))
    
    # Spout
    pygame.draw.rect(surface, (135, 206, 235), (4, 10, 4, 4))
    
    # Water drops
    drops = [(6, 20), (4, 24), (8, 22)]
    for x, y in drops:
        pygame.draw.rect(surface, (0, 191, 255), (x, y, 2, 2))
    
    return surface

def create_seed_icon():
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    
    # Seed bag
    pygame.draw.rect(surface, (205, 133, 63), (8, 8, 16, 16))
    pygame.draw.rect(surface, (139, 69, 19), (8, 16, 16, 8))
    
    # Seeds
    seeds = [(12, 12), (16, 14), (20, 12), (14, 16), (18, 16)]
    for x, y in seeds:
        pygame.draw.rect(surface, (34, 139, 34), (x, y, 2, 2))
    
    return surface

def create_harvest_icon():
    surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    
    # Basket
    pygame.draw.rect(surface, (218, 165, 32), (8, 16, 16, 8))
    pygame.draw.rect(surface, (184, 134, 11), (6, 20, 20, 4))
    
    # Produce
    pygame.draw.circle(surface, (255, 0, 0), (12, 14), 3)  # Red fruit
    pygame.draw.circle(surface, (255, 255, 0), (16, 12), 3)  # Yellow fruit
    pygame.draw.circle(surface, (255, 165, 0), (20, 14), 3)  # Orange fruit
    
    return surface

# Generate and save icons
icons = {
    "hoe": create_hoe_icon(),
    "water": create_water_icon(),
    "seed": create_seed_icon(),
    "harvest": create_harvest_icon()
}

for name, surface in icons.items():
    pygame.image.save(surface, os.path.join("assets", "ui", f"{name}.png"))

pygame.quit() 