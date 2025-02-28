import pygame
from game.items import Items, ItemStack
from game.ui import Tool
from game.sprites import CharacterSprite

class Player:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.speed = 200  # pixels per second
        self.selected_tool = Tool.HOE
        self.inventory = []
        self.facing = 'down'  # can be 'up', 'down', 'left', 'right'
        
        # Initialize sprite
        self.sprite = CharacterSprite(scale=1.5)  # Scale up for better visibility
        self.last_movement = pygame.time.get_ticks()
        self.is_moving = False
        self.is_using_tool = False
        self.tool_start_time = 0
        self.tool_duration = 600  # milliseconds for tool animation
        
        # Add some starting items
        self.inventory.append(ItemStack(Items.CARROT_SEEDS, 5))
        self.inventory.append(ItemStack(Items.TOMATO_SEEDS, 5))
        self.inventory.append(ItemStack(Items.POTATO_SEEDS, 5))

    def update(self, dt, keys):
        current_time = pygame.time.get_ticks()
        
        # Only allow movement if not using a tool
        if not self.is_using_tool:
            # Handle movement
            dx = dy = 0
            if keys[pygame.K_w]:
                dy = -1
                self.facing = 'up'
            if keys[pygame.K_s]:
                dy = 1
                self.facing = 'down'
            if keys[pygame.K_a]:
                dx = -1
                self.facing = 'left'
            if keys[pygame.K_d]:
                dx = 1
                self.facing = 'right'

            # Normalize diagonal movement
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071

            # Calculate new position
            new_x = self.x + dx * self.speed * dt / 1000
            new_y = self.y + dy * self.speed * dt / 1000

            # Get grid coordinates for new position
            grid_x = int(new_x / self.world.tile_size)
            grid_y = int(new_y / self.world.tile_size)

            # Check if new position is walkable
            if self.world.is_walkable(grid_x, grid_y):
                self.x = new_x
                self.y = new_y
                
            # Update sprite state based on movement
            self.is_moving = dx != 0 or dy != 0
            if self.is_moving:
                self.sprite.set_state('walk', self.facing)
            else:
                self.sprite.set_state('idle', self.facing)
        
        # Update tool animation
        if self.is_using_tool:
            if current_time - self.tool_start_time >= self.tool_duration:
                self.is_using_tool = False
                self.sprite.set_state('idle', self.facing)

    def get_target_tile(self):
        # Get the tile in front of the player based on facing direction
        grid_x = int(self.x / self.world.tile_size)
        grid_y = int(self.y / self.world.tile_size)
        
        if self.facing == 'up':
            grid_y -= 1
        elif self.facing == 'down':
            grid_y += 1
        elif self.facing == 'left':
            grid_x -= 1
        elif self.facing == 'right':
            grid_x += 1
            
        return grid_x, grid_y

    def use_tool(self):
        if self.is_using_tool:
            return False
            
        grid_x, grid_y = self.get_target_tile()
        tile = self.world.get_tile(grid_x, grid_y)
        
        if tile is None:
            return False
            
        tool_used = False
        if self.selected_tool == Tool.HOE:
            if tile == self.world.Tile.SOIL:
                self.world.set_tile(grid_x, grid_y, self.world.Tile.TILLED_SOIL)
                tool_used = True
                
        elif self.selected_tool == Tool.WATER:
            tool_used = self.world.water_tile(grid_x, grid_y)
                
        elif self.selected_tool == Tool.SEED:
            # Find seeds in inventory
            for item in self.inventory:
                if "_SEEDS" in item.item_type.id:
                    if item.quantity > 0 and self.world.plant_seed(grid_x, grid_y, item.item_type):
                        item.remove(1)
                        tool_used = True
                    break
                    
        elif self.selected_tool == Tool.HARVEST:
            harvested = self.world.harvest_plant(grid_x, grid_y)
            if harvested:
                # Convert seed type to produce type
                produce_id = harvested.item_type.id.replace("_SEEDS", "")
                produce_type = getattr(Items, produce_id)
                
                # Find existing stack or create new one
                for item in self.inventory:
                    if item.item_type == produce_type:
                        item.add(1)
                        break
                else:
                    self.inventory.append(ItemStack(produce_type, 1))
                tool_used = True
        
        if tool_used:
            # Start tool animation
            self.is_using_tool = True
            self.tool_start_time = pygame.time.get_ticks()
            self.sprite.set_state(self.selected_tool, self.facing)
            
        return tool_used

    def draw(self, screen, camera_x=0, camera_y=0):
        # Get current sprite frame
        current_frame = self.sprite.update(pygame.time.get_ticks())
        
        # Calculate screen position
        screen_x = int(self.x - camera_x - current_frame.get_width() // 2)
        screen_y = int(self.y - camera_y - current_frame.get_height() * 0.75)
        
        # Draw sprite
        screen.blit(current_frame, (screen_x, screen_y)) 