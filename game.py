import math
import pygame
from settings import *
from bird import Bird
from pipe import Pipe
from population import Population

class Game:
    def __init__(self, high_score_in=0, mode="manual"):
        self.bg = pygame.transform.scale(
            pygame.image.load("background2.png").convert(),
            (WIN_WIDTH, WIN_HEIGHT - GROUND_HEIGHT)
        )

        self.ground_img = pygame.transform.scale(
            pygame.image.load("ground.png").convert_alpha(),
            (WIN_WIDTH, GROUND_HEIGHT)
        )
        self.ground_x = 0

        self.get_ready_img = pygame.transform.scale(
            pygame.image.load("ready.png").convert_alpha(), (300, 100)
        )
        self.press_img = pygame.transform.scale(
            pygame.image.load("press.png").convert_alpha(), (200, 200)
        )

        self.mode = mode
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.score_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.game_over_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.stat_font = pygame.font.SysFont("Arial", 28)

        self.high_score = high_score_in
        self.game_state = "menu"

        self.population = Population(size=50) if self.mode == "auto" else None

        self.reset_round()


    def reset_round(self):
        self.pipes = []
        self.frame = 0
        self.medal_image = None
        self.pipes_passed_gen = 0
        self.ground_x = 0

        if self.mode == "manual":
            self.bird = Bird()
            self.game_state = "get_ready"
        else:
            self.bird = None
            self.game_state = "playing"
            self.pipes.append(Pipe(WIN_WIDTH + 50))
            self.pipes.append(Pipe(WIN_WIDTH + 250))


    def spawn_pipe(self):
        last_x = self.pipes[-1].x if self.pipes else WIN_WIDTH
        self.pipes.append(Pipe(last_x + 200))


    def update(self):
        if self.game_state == "get_ready":
            self.bird.y = WIN_HEIGHT // 2 + 10 * math.sin(pygame.time.get_ticks() * 0.005)
            self.ground_x -= PIPE_VEL
            if self.ground_x <= -WIN_WIDTH:
                self.ground_x = 0
            return

        if self.mode == "auto":
            if all(not b.alive for b in self.population.birds):
                self.population.evolve()
                self.reset_round()
                return

        if self.game_state != "playing":
            return

        self.ground_x -= PIPE_VEL
        if self.ground_x <= -WIN_WIDTH:
            self.ground_x = 0

        self.frame += 1
        if self.frame % 45 == 0:
            self.spawn_pipe()

        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.x < -PIPE_WIDTH:
                self.pipes.remove(pipe)

        birds = (
            [self.bird] if self.mode == "manual"
            else [b for b in self.population.birds if b.alive]
        )

        for bird in birds:
            if self.mode == "auto" and self.pipes:
                bird.think(self.pipes)

            bird.update()

            if self.mode == "auto":
                bird.fitness += 1  

            if bird.y + BIRD_RADIUS >= GROUND_Y or bird.y < 0:
                bird.alive = False
                if self.mode == "auto":
                    bird.fitness += bird.score * 100
                continue

            for pipe in self.pipes:
                hit, scored = pipe.collides(bird)

                if hit:
                    bird.alive = False
                    if self.mode == "auto":
                        bird.fitness += bird.score * 100
                    break

                if scored:
                    bird.score += 1
                    if self.mode == "auto":
                        bird.fitness += 100
                        self.pipes_passed_gen = max(self.pipes_passed_gen, bird.score)

        if self.mode == "manual" and not self.bird.alive:
            self.game_state = "game_over"
            self.high_score = max(self.high_score, self.bird.score)
            self.medal_image = self.get_medal(self.bird.score)

    def get_medal(self, score):
        if score >= 40:
            return pygame.transform.scale(pygame.image.load("platinum_medal.png").convert_alpha(), (80, 80))
        if score >= 30:
            return pygame.transform.scale(pygame.image.load("gold_medal.png").convert_alpha(), (80, 80))
        if score >= 20:
            return pygame.transform.scale(pygame.image.load("silver_medal.png").convert_alpha(), (80, 80))
        if score >= 10:
            return pygame.transform.scale(pygame.image.load("bronze_medal.png").convert_alpha(), (80, 80))
        return None


    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.ground_img, (self.ground_x, GROUND_Y))
        self.screen.blit(self.ground_img, (self.ground_x + WIN_WIDTH, GROUND_Y))

        if self.game_state == "get_ready":
            self.bird.draw(self.screen)
            self.screen.blit(self.get_ready_img, self.get_ready_img.get_rect(midtop=(WIN_WIDTH//2, 80)))
            self.screen.blit(self.press_img, self.press_img.get_rect(midtop=(190, 230)))

        elif self.game_state == "playing":
            for pipe in self.pipes:
                pipe.draw(self.screen)

            if self.mode == "manual":
                self.bird.draw(self.screen)
                score = self.score_font.render(str(self.bird.score), True, (255, 255, 255))
                self.screen.blit(score, (WIN_WIDTH//2 - score.get_width()//2, 10))
            else:
                for bird in self.population.birds:
                    if bird.alive:
                        bird.draw(self.screen)

                alive = sum(b.alive for b in self.population.birds)
                self.screen.blit(self.stat_font.render(f"Gen: {self.population.generation}", True, (255,255,255)), (10,10))
                self.screen.blit(self.stat_font.render(f"Pipes: {self.pipes_passed_gen}", True, (255,255,255)), (10,40))
                self.screen.blit(self.stat_font.render(f"Alive: {alive}/{self.population.size}", True, (255,255,255)), (10,70))
                self.screen.blit(self.stat_font.render(f"Best Fit: {int(self.population.best_fitness)}", True, (255,255,255)), (10,100))

        elif self.game_state == "game_over":
            for pipe in self.pipes:
                pipe.draw(self.screen)

            card = pygame.Rect(WIN_WIDTH//2 - 150, WIN_HEIGHT//2 - 150, 300, 300)
            pygame.draw.rect(self.screen, (255,255,255), card, border_radius=10)
            pygame.draw.rect(self.screen, (0,0,0), card, 5, border_radius=10)

            title = self.game_over_font.render("GAME OVER", True, (255,0,0))
            self.screen.blit(title, (WIN_WIDTH//2 - title.get_width()//2, WIN_HEIGHT//2 - 130))

            score = self.stat_font.render(f"Score: {self.bird.score}", True, (0,0,0))
            best = self.stat_font.render(f"Best: {self.high_score}", True, (0,0,0))
            self.screen.blit(score, (WIN_WIDTH//2 - score.get_width()//2, WIN_HEIGHT//2 + 50))
            self.screen.blit(best, (WIN_WIDTH//2 - best.get_width()//2, WIN_HEIGHT//2 + 90))

            if self.medal_image:
                self.screen.blit(self.medal_image, self.medal_image.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2 - 30)))

        pygame.display.flip()


    def run(self):
        while True:
            self.clock.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self.high_score

                if self.mode == "manual" and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        if self.game_state == "get_ready":
                            self.game_state = "playing"
                            self.pipes.append(Pipe(WIN_WIDTH + 50))
                        elif self.game_state == "playing" and self.bird.alive:
                            self.bird.flap()
                        elif self.game_state == "game_over":
                            self.reset_round()

                    if e.key == pygame.K_ESCAPE:
                        return self.high_score

            self.update()
            self.draw()
