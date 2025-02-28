import pygame
import os
import math

# Initialize Pygame
pygame.init()

# Constants
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48
COLORS = {
    'skin': (255, 223, 196),      # Light skin tone
    'hair': (139, 69, 19),        # Brown hair
    'shirt': (30, 144, 255),      # Bright blue
    'pants': (47, 79, 79),        # Dark slate gray
    'shoes': (101, 67, 33),       # Dark brown
    'tool_metal': (192, 192, 192), # Silver
    'tool_wood': (139, 69, 19),    # Brown
    'water': (0, 191, 255),        # Deep sky blue
    'seed': (34, 139, 34)         # Forest green
}

def create_character_base(surface, direction):
    """Draw the basic character shape"""
    # Head
    pygame.draw.ellipse(surface, COLORS['skin'], 
                       (SPRITE_WIDTH//4, 2, SPRITE_WIDTH//2, SPRITE_WIDTH//2))
    
    # Body
    body_top = SPRITE_WIDTH//2
    pygame.draw.rect(surface, COLORS['shirt'],
                    (SPRITE_WIDTH//4, body_top, SPRITE_WIDTH//2, SPRITE_HEIGHT//3))
    
    # Legs
    leg_top = body_top + SPRITE_HEIGHT//3
    leg_width = SPRITE_WIDTH//4
    if direction == 'down' or direction == 'up':
        # Left leg
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//4, leg_top, leg_width, SPRITE_HEIGHT//3))
        # Right leg
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//2, leg_top, leg_width, SPRITE_HEIGHT//3))
    else:
        # Single leg for side view
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//3, leg_top, leg_width, SPRITE_HEIGHT//3))
    
    # Shoes
    shoe_top = leg_top + SPRITE_HEIGHT//3 - 4
    if direction == 'down' or direction == 'up':
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//4-2, shoe_top, leg_width+2, 4))
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//2, shoe_top, leg_width+2, 4))
    else:
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//3-2, shoe_top, leg_width+4, 4))

def create_tool_animation(base_surface, tool_type, frame, direction):
    """Add tool animation to character base"""
    surface = base_surface.copy()
    
    if tool_type == 'hoe':
        # Draw hoe with animation
        handle_pos = [(SPRITE_WIDTH*3//4, SPRITE_HEIGHT//2),
                     (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//3),
                     (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//4)]
        
        angle = frame * 30  # 30 degree rotation per frame
        
        # Draw handle
        pygame.draw.line(surface, COLORS['tool_wood'],
                        handle_pos[frame],
                        (handle_pos[frame][0] - math.cos(math.radians(angle))*20,
                         handle_pos[frame][1] - math.sin(math.radians(angle))*20),
                        3)
        
        # Draw blade
        pygame.draw.line(surface, COLORS['tool_metal'],
                        (handle_pos[frame][0] - math.cos(math.radians(angle))*15,
                         handle_pos[frame][1] - math.sin(math.radians(angle))*15),
                        (handle_pos[frame][0] - math.cos(math.radians(angle+45))*8,
                         handle_pos[frame][1] - math.sin(math.radians(angle+45))*8),
                        2)
    
    elif tool_type == 'water':
        # Draw watering can with animation
        can_pos = [(SPRITE_WIDTH*3//4, SPRITE_HEIGHT//2),
                  (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//3),
                  (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//4)]
        
        # Draw can body
        pygame.draw.rect(surface, COLORS['tool_metal'],
                        (can_pos[frame][0]-8, can_pos[frame][1]-4, 12, 8))
        
        # Draw spout
        pygame.draw.line(surface, COLORS['tool_metal'],
                        (can_pos[frame][0]+4, can_pos[frame][1]),
                        (can_pos[frame][0]+8, can_pos[frame][1]-6),
                        2)
        
        # Draw water drops
        if frame > 0:
            for i in range(3):
                drop_x = can_pos[frame][0] + 8 + i*4
                drop_y = can_pos[frame][1] - 4 + frame*4
                pygame.draw.circle(surface, COLORS['water'],
                                (drop_x, drop_y), 1)
    
    elif tool_type == 'seed':
        # Draw seed bag and seeds
        bag_pos = [(SPRITE_WIDTH*3//4, SPRITE_HEIGHT//2),
                  (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//3),
                  (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//4)]
        
        # Draw bag
        pygame.draw.rect(surface, COLORS['tool_wood'],
                        (bag_pos[frame][0]-6, bag_pos[frame][1]-8, 10, 12))
        
        # Draw seeds
        if frame > 0:
            for i in range(frame):
                seed_x = bag_pos[frame][0] + i*4
                seed_y = bag_pos[frame][1] + 8
                pygame.draw.circle(surface, COLORS['seed'],
                                (seed_x, seed_y), 1)
    
    elif tool_type == 'harvest':
        # Draw harvesting animation
        hand_pos = [(SPRITE_WIDTH*3//4, SPRITE_HEIGHT//2),
                   (SPRITE_WIDTH*3//4, SPRITE_HEIGHT//3),
                   (SPRITE_WIDTH*2//3, SPRITE_HEIGHT//3)]
        
        # Draw arm
        pygame.draw.line(surface, COLORS['skin'],
                        (SPRITE_WIDTH//2, SPRITE_HEIGHT//2),
                        hand_pos[frame],
                        4)
    
    return surface

def create_walk_animation(base_surface, frame, direction):
    """Add walking animation to character base"""
    surface = base_surface.copy()
    
    # Animate legs
    leg_top = SPRITE_HEIGHT//2 + SPRITE_HEIGHT//3
    leg_width = SPRITE_WIDTH//4
    
    if direction == 'down' or direction == 'up':
        # Calculate leg positions based on frame
        left_offset = math.sin(frame * math.pi/2) * 4
        right_offset = -math.sin(frame * math.pi/2) * 4
        
        # Left leg
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//4, leg_top + left_offset, 
                         leg_width, SPRITE_HEIGHT//3 - abs(left_offset)))
        # Right leg
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//2, leg_top + right_offset,
                         leg_width, SPRITE_HEIGHT//3 - abs(right_offset)))
        
        # Shoes
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//4-2, leg_top + left_offset + SPRITE_HEIGHT//3 - 4,
                         leg_width+2, 4))
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//2, leg_top + right_offset + SPRITE_HEIGHT//3 - 4,
                         leg_width+2, 4))
    else:
        # Side view walking
        offset = math.sin(frame * math.pi/2) * 4
        pygame.draw.rect(surface, COLORS['pants'],
                        (SPRITE_WIDTH//3, leg_top + offset,
                         leg_width, SPRITE_HEIGHT//3 - abs(offset)))
        pygame.draw.rect(surface, COLORS['shoes'],
                        (SPRITE_WIDTH//3-2, leg_top + offset + SPRITE_HEIGHT//3 - 4,
                         leg_width+4, 4))
    
    return surface

def create_sprite_sheet():
    """Create the complete character sprite sheet"""
    # Calculate sprite sheet size
    states = ['idle', 'walk', 'hoe', 'water', 'seed', 'harvest']
    directions = ['down', 'left', 'right', 'up']
    max_frames = 4  # Maximum frames for any animation
    
    sheet_width = SPRITE_WIDTH * max_frames
    sheet_height = SPRITE_HEIGHT * len(directions) * len(states)
    
    # Create sprite sheet surface
    sprite_sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    
    # Generate all animations
    for state_idx, state in enumerate(states):
        for dir_idx, direction in enumerate(directions):
            # Calculate base position in sprite sheet
            base_x = 0
            base_y = (state_idx * len(directions) + dir_idx) * SPRITE_HEIGHT
            
            # Number of frames for this animation
            frames = 4 if state in ['idle', 'walk'] else 3
            
            for frame in range(frames):
                # Create frame surface
                frame_surface = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT), 
                                            pygame.SRCALPHA)
                
                # Draw base character
                create_character_base(frame_surface, direction)
                
                # Add animation based on state
                if state == 'walk':
                    frame_surface = create_walk_animation(frame_surface, frame, 
                                                        direction)
                elif state in ['hoe', 'water', 'seed', 'harvest']:
                    frame_surface = create_tool_animation(frame_surface, state, 
                                                        frame, direction)
                
                # Add to sprite sheet
                sprite_sheet.blit(frame_surface, 
                                (base_x + frame * SPRITE_WIDTH, base_y))
    
    return sprite_sheet

def main():
    # Create output directory if it doesn't exist
    os.makedirs(os.path.join("assets", "sprites"), exist_ok=True)
    
    # Generate sprite sheet
    sprite_sheet = create_sprite_sheet()
    
    # Save sprite sheet
    output_path = os.path.join("assets", "sprites", "character.png")
    pygame.image.save(sprite_sheet, output_path)
    print(f"Character sprite sheet saved to {output_path}")

if __name__ == "__main__":
    main()
    pygame.quit() 