import pygame
import random
from circleshape import CircleShape 
from constants import *

class PowerUp(pygame.sprite.Sprite):

    TYPES = ["fast_shoot", "double_shot"]

    containers = None  

    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.size = 20  
        self.type = random.choice(self.TYPES)

    def draw(self, screen):
        color = "yellow" if self.type == "fast_shoot" else "cyan"
        rect = pygame.Rect(self.position.x - self.size / 2,
                           self.position.y - self.size / 2,
                           self.size, self.size)
        pygame.draw.rect(screen, color, rect, LINE_WIDTH)

    def update(self, dt):
        
        pass