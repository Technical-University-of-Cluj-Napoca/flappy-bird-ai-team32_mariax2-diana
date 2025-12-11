import pygame
import random
from settings import *

def clamp(v, a, b):
    return max(a, min(v, b))

def bird_pipe_collision(birdx, birdy, r, pipe):
    x = clamp(birdx, pipe.left, pipe.right)
    y = clamp(birdy, pipe.top, pipe.bottom)
    return (birdx - x) ** 2 + (birdy - y) ** 2 <= r * r

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(130, WIN_HEIGHT - 130)
        self.passed = False

    def update(self):
        self.x -= PIPE_VEL

    def collides(self, bird):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP//2)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP//2, PIPE_WIDTH, WIN_HEIGHT)
        return (
            bird_pipe_collision(bird.x, bird.y, BIRD_RADIUS, top_rect) or
            bird_pipe_collision(bird.x, bird.y, BIRD_RADIUS, bottom_rect)
        )

    def draw(self, surf):
        pygame.draw.rect(surf, (25, 0, 51), (self.x, 0, PIPE_WIDTH, self.gap_y - PIPE_GAP//2))
        pygame.draw.rect(surf, (25, 0, 51), (self.x, self.gap_y + PIPE_GAP//2, PIPE_WIDTH, WIN_HEIGHT))
