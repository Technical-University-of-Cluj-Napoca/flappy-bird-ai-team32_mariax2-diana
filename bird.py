import pygame
from settings import *

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = WIN_HEIGHT / 2
        self.vel = 0
        self.alive = True
        self.score = 0
        self.img_up = pygame.image.load("bird_up.png").convert_alpha()
        self.img_down = pygame.image.load("bird_down.png").convert_alpha()

        self.img_up = pygame.transform.scale(self.img_up, (40, 30))
        self.img_down = pygame.transform.scale(self.img_down, (40, 30))
        self.img_up.set_colorkey((255, 255, 255))
        self.img_down.set_colorkey((255, 255, 255))

    def flap(self):
        self.vel = -7

    def update(self):
        self.vel += 0.5     
        self.y += self.vel 

    def draw(self, surf):
        if self.vel < 0:
            img = self.img_up
        else:        
            img = self.img_down
            
        rect = img.get_rect(center=(self.x, self.y))
        surf.blit(img, rect)
