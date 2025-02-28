import pygame

class Tool:
    HOE = "hoe"
    WATER = "water"
    SEED = "seed"
    HARVEST = "harvest"

    @staticmethod
    def get_color(tool_type):
        colors = {
            Tool.HOE: (139, 69, 19),      # Brown
            Tool.WATER: (0, 191, 255),     # Deep Sky Blue
            Tool.SEED: (34, 139, 34),      # Forest Green
            Tool.HARVEST: (218, 165, 32),  # Golden Rod
        }
        return colors.get(tool_type, (128, 128, 128))

class ToolBar:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.slot_size = 50
        self.padding = 5
        self.slots = [Tool.HOE, Tool.WATER, Tool.SEED, Tool.HARVEST]
        self.selected_slot = 0
        
        # Position the toolbar at the bottom center
        self.total_width = (self.slot_size + self.padding) * len(self.slots) - self.padding
        self.x = (screen_width - self.total_width) // 2
        self.y = screen_height - self.slot_size - 10
        
        # Create font for hotkey numbers
        self.font = pygame.font.Font(None, 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Number keys 1-4 for tool selection
            if pygame.K_1 <= event.key <= pygame.K_1 + len(self.slots) - 1:
                self.selected_slot = event.key - pygame.K_1
                return True
        return False

    def get_selected_tool(self):
        return self.slots[self.selected_slot]

    def draw(self, screen):
        for i, tool in enumerate(self.slots):
            # Calculate position
            x = self.x + (self.slot_size + self.padding) * i
            rect = pygame.Rect(x, self.y, self.slot_size, self.slot_size)
            
            # Draw slot background
            pygame.draw.rect(screen, (64, 64, 64), rect)
            
            # Draw tool icon (using color for now, will be replaced with sprites)
            inner_rect = pygame.Rect(x + 5, self.y + 5, self.slot_size - 10, self.slot_size - 10)
            pygame.draw.rect(screen, Tool.get_color(tool), inner_rect)
            
            # Draw selection highlight
            if i == self.selected_slot:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            else:
                pygame.draw.rect(screen, (128, 128, 128), rect, 1)
            
            # Draw hotkey number
            number_text = self.font.render(str(i + 1), True, (255, 255, 255))
            number_rect = number_text.get_rect(bottomright=(x + self.slot_size - 2, self.y + self.slot_size - 2))
            screen.blit(number_text, number_rect)

class StatusPanel:
    def __init__(self, screen_width):
        self.width = 200
        self.height = 60
        self.x = 10
        self.y = 10
        self.font = pygame.font.Font(None, 24)
        
        # Game state
        self.money = 100
        self.day = 1
        self.time = 0  # 0-24 hours
        
    def update(self, dt):
        # Update time (1 real second = 1 game minute)
        self.time += dt / 1000 * 60
        if self.time >= 24 * 60:  # New day
            self.time = 0
            self.day += 1

    def draw(self, screen):
        # Draw panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0, 128), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 1)
        
        # Draw money
        money_text = self.font.render(f"${self.money}", True, (255, 255, 0))
        screen.blit(money_text, (self.x + 10, self.y + 10))
        
        # Draw time
        hours = int(self.time // 60)
        minutes = int(self.time % 60)
        time_text = self.font.render(f"{hours:02d}:{minutes:02d}", True, (255, 255, 255))
        screen.blit(time_text, (self.x + 10, self.y + 35))
        
        # Draw day
        day_text = self.font.render(f"Day {self.day}", True, (255, 255, 255))
        day_rect = day_text.get_rect(topright=(self.x + self.width - 10, self.y + 10))
        screen.blit(day_text, day_rect) 