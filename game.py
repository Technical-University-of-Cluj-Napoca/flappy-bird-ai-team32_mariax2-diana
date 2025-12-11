import pygame
from settings import *
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_round()

    def reset_round(self):
        self.bird = Bird()
        self.pipes = [Pipe(WIN_WIDTH + 50)]
        self.frame = 0

    def spawn_pipe(self):
        last_x = self.pipes[-1].x
        self.pipes.append(Pipe(last_x + 200))

    def update(self):
        self.frame += 1
        if self.frame % 60 == 0:
            self.spawn_pipe()

        for p in list(self.pipes):
            p.update()
            if p.x < -PIPE_WIDTH:
                self.pipes.remove(p)

        if self.bird.alive:
            self.bird.update()

            if self.bird.y > WIN_HEIGHT - 40 or self.bird.y < 0:
                self.bird.alive = False

            for p in self.pipes:
                if p.collides(self.bird):
                    self.bird.alive = False
        else:
            self.reset_round()

    def draw(self):
        self.screen.fill((150, 200, 250))

        for p in self.pipes:
            p.draw(self.screen)

        self.bird.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                    if e.key == pygame.K_SPACE and self.bird.alive:
                        self.bird.flap()

            self.update()
            self.draw()

        pygame.quit()
