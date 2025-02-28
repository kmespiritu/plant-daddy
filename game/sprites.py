import pygame
import os
from typing import Dict, List, Tuple

class Animation:
    def __init__(self, frames: List[pygame.Surface], frame_duration: int = 100):
        """
        Initialize an animation
        frames: List of surfaces for each frame
        frame_duration: Duration of each frame in milliseconds
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = 0
        self.is_playing = True
        
    def update(self, current_time: int) -> pygame.Surface:
        """Update animation and return current frame"""
        if not self.is_playing:
            return self.frames[self.current_frame]
            
        if current_time - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = current_time
            
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.is_playing = True
        
    def pause(self):
        """Pause the animation"""
        self.is_playing = False
        
    def resume(self):
        """Resume the animation"""
        self.is_playing = True

class CharacterSprite:
    def __init__(self, scale: float = 1.0):
        """
        Initialize character sprite with all animations
        scale: Scale factor for the sprite (1.0 = original size)
        """
        self.scale = scale
        self.facing = 'down'
        self.state = 'idle'
        self.animations: Dict[str, Dict[str, Animation]] = {
            'idle': {},
            'walk': {},
            'hoe': {},
            'water': {},
            'seed': {},
            'harvest': {}
        }
        
        # Load all character animations
        self.load_animations()
        
    def load_animations(self):
        """Load all character animations from the assets folder"""
        sprite_size = (32, 48)  # Base sprite size before scaling
        
        # Define animation frame counts for each state
        frame_counts = {
            'idle': 4,
            'walk': 4,
            'hoe': 3,
            'water': 3,
            'seed': 3,
            'harvest': 3
        }
        
        # Define animation speeds (milliseconds per frame)
        frame_durations = {
            'idle': 400,
            'walk': 150,
            'hoe': 200,
            'water': 200,
            'seed': 200,
            'harvest': 200
        }
        
        # Load sprite sheet
        sprite_sheet_path = os.path.join("assets", "sprites", "character.png")
        if not os.path.exists(sprite_sheet_path):
            raise FileNotFoundError(f"Could not find sprite sheet at {sprite_sheet_path}")
            
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        # Define directions and their row in the sprite sheet
        directions = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }
        
        # For each state and direction, create animation
        for state in self.animations.keys():
            state_offset = list(self.animations.keys()).index(state) * 4  # 4 directions per state
            
            for direction, row in directions.items():
                frames = []
                for frame in range(frame_counts[state]):
                    # Calculate position in sprite sheet
                    x = frame * sprite_size[0]
                    y = (row + state_offset) * sprite_size[1]
                    
                    # Extract frame from sprite sheet
                    frame_surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
                    frame_surface.blit(sprite_sheet, (0, 0), 
                                     (x, y, sprite_size[0], sprite_size[1]))
                    
                    # Scale if needed
                    if self.scale != 1.0:
                        new_size = (int(sprite_size[0] * self.scale), 
                                  int(sprite_size[1] * self.scale))
                        frame_surface = pygame.transform.scale(frame_surface, new_size)
                    
                    frames.append(frame_surface)
                
                # Create animation for this state and direction
                self.animations[state][direction] = Animation(
                    frames, frame_durations[state]
                )
    
    def update(self, current_time: int) -> pygame.Surface:
        """Update current animation and return current frame"""
        return self.animations[self.state][self.facing].update(current_time)
    
    def set_state(self, state: str, facing: str = None):
        """
        Change animation state and optionally facing direction
        Resets the animation if state changes
        """
        if state not in self.animations:
            raise ValueError(f"Invalid state: {state}")
            
        if facing and facing not in self.animations[state]:
            raise ValueError(f"Invalid facing direction: {facing}")
            
        if state != self.state:
            self.state = state
            self.animations[state][self.facing].reset()
            
        if facing and facing != self.facing:
            self.facing = facing
            self.animations[self.state][facing].reset()
    
    def get_size(self) -> Tuple[int, int]:
        """Get current sprite size"""
        current_frame = self.animations[self.state][self.facing].frames[0]
        return current_frame.get_size() 