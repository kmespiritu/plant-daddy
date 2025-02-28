import pygame
import os
from dataclasses import dataclass

@dataclass
class ItemType:
    id: str
    name: str
    icon_path: str = None
    max_stack: int = 99
    
    def __post_init__(self):
        if self.icon_path and os.path.exists(self.icon_path):
            self._icon = pygame.image.load(self.icon_path)
        else:
            self._icon = None
    
    @property
    def icon(self):
        return self._icon

class Items:
    # Seeds
    CARROT_SEEDS = ItemType("carrot_seeds", "Carrot Seeds", max_stack=99)
    TOMATO_SEEDS = ItemType("tomato_seeds", "Tomato Seeds", max_stack=99)
    POTATO_SEEDS = ItemType("potato_seeds", "Potato Seeds", max_stack=99)
    
    # Produce
    CARROT = ItemType("carrot", "Carrot", max_stack=99)
    TOMATO = ItemType("tomato", "Tomato", max_stack=99)
    POTATO = ItemType("potato", "Potato", max_stack=99)
    
    @classmethod
    def get_all_items(cls):
        return [value for name, value in vars(cls).items() 
                if isinstance(value, ItemType)]

@dataclass
class ItemStack:
    item_type: ItemType
    quantity: int = 1
    
    def add(self, amount):
        self.quantity = min(self.quantity + amount, self.item_type.max_stack)
        return self.quantity
    
    def remove(self, amount):
        if amount >= self.quantity:
            removed = self.quantity
            self.quantity = 0
            return removed
        self.quantity -= amount
        return amount 