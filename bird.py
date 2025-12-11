import pygame
from settings import *

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = WIN_HEIGHT / 2
        self.vel = 0
        self.alive = True
        self.score = 0

    def flap(self):
        self.vel = -7

    def update(self):
        self.vel += 0.5     
        self.y += self.vel 

    def draw(self, surf):
        pygame.draw.circle(
            surf, (255, 255, 0), 
            (int(self.x), int(self.y)), 
            BIRD_RADIUS
        )
