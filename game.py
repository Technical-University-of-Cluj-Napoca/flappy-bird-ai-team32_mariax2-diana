import math
import pygame
from settings import *
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self, high_score_in = 0, mode = "manual"):
        self.bg = pygame.transform.scale(
        pygame.image.load("background2.png").convert(),
        (WIN_WIDTH, WIN_HEIGHT)
        )

        self.get_ready_img = pygame.image.load("ready.png").convert_alpha()
        self.get_ready_img = pygame.transform.scale(self.get_ready_img, (300, 100))
        self.press_img = pygame.image.load("press.png").convert_alpha()
        self.press_img = pygame.transform.scale(self.press_img, (200, 200))


        self.mode = mode
        
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()

        if not pygame.font.get_init():
            self.font.init()
        self.score_font = pygame.font.SysFont("Arial", 40, bold = True)
        self.game_over_font = pygame.font.SysFont("Arial", 60, bold = True)
        self.stat_font = pygame.font.SysFont("Arial", 28)

        self.high_score = high_score_in
        self.game_state = "menu"
        self.medal_image = None

        self.load_medal_images()
        self.reset_round()
    
    def load_medal_images(self):
        self.medals = {
            "bronze": pygame.image.load("bronze_medal.png").convert_alpha(),
            "silver": pygame.image.load("silver_medal.png").convert_alpha(),
            "gold": pygame.image.load("gold_medal.png").convert_alpha(),
            "platinum": pygame.image.load("platinum_medal.png").convert_alpha(),
            "none": None
        }
        for key in self.medals:
            if self.medals[key] is not None:
                self.medals[key] = pygame.transform.scale(self.medals[key], (80, 80))
        
    def reset_round(self):
        self.bird = Bird()
        self.pipes = []
        self.frame = 0
        self.game_state = "get_ready"
        self.medal_image = None

    def get_medal(self, score):
        if score >= 40:
            return self.medals["platinum"]
        elif score >= 30:
            return self.medals["gold"]
        elif score >= 20:
            return self.medals["silver"]
        elif score >= 10:
            return self.medals["bronze"]
        return self.medals["none"]

    def spawn_pipe(self):
        if not self.pipes:
            self.pipes.append(Pipe(WIN_WIDTH + 50))
        else:
            last_x = self.pipes[-1].x
            self.pipes.append(Pipe(last_x + 200))

    def update(self):
        if self.game_state == "get_ready":
            self.bird.y = WIN_HEIGHT // 2 + 10 * math.sin(pygame.time.get_ticks() * 0.005)
            return
        
        if self.game_state != "playing":
            return 

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
                collision_status, scored_point = p.collides(self.bird)

                if collision_status:
                    self.bird.alive = False

                if scored_point: 
                    self.bird.score += 1
        else:
            if self.game_state == "playing":
                self.game_state = "game_over"
                self.high_score = max(self.high_score, self.bird.score)
                self.medal_image = self.get_medal(self.bird.score)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        if self.game_state == "get_ready":
            self.bird.draw(self.screen)
            rect = self.get_ready_img.get_rect(midtop=(WIN_WIDTH // 2, 80))
            self.screen.blit(self.get_ready_img, rect)
            rect = self.press_img.get_rect(midtop =(190, 230))
            self.screen.blit(self.press_img, rect)

        elif self.game_state == "playing":
            for p in self.pipes:
                p.draw(self.screen)

            self.bird.draw(self.screen)

            score_text = self.score_font.render(str(self.bird.score), True, (255, 255, 255))
            score_shadow = self.score_font.render(str(self.bird.score), True, (0, 0, 0)) 

            self.screen.blit(score_shadow, (WIN_WIDTH // 2 - score_text.get_width() // 2 + 2, 10 + 2))
            self.screen.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, 10))

        if self.game_state == "game_over":
            card_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 150, 300, 300)
            pygame.draw.rect(self.screen, (255, 255, 255), card_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), card_rect, 5, border_radius=10)

            title = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, WIN_HEIGHT // 2 - 130))

            current_score_text = self.stat_font.render(f"Score: {self.bird.score}", True, (0, 0, 0))
            best_score_text = self.stat_font.render(f"Best: {self.high_score}", True, (0, 0, 0))
                    
            self.screen.blit(current_score_text, (WIN_WIDTH // 2 - current_score_text.get_width() // 2, WIN_HEIGHT // 2 + 50))
            self.screen.blit(best_score_text, (WIN_WIDTH // 2 - best_score_text.get_width() // 2, WIN_HEIGHT // 2 + 90))


            if self.medal_image:
                medal_rect = self.medal_image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 30))
                self.screen.blit(self.medal_image, medal_rect)
                
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return self.high_score
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return self.high_score
                    if e.key == pygame.K_SPACE:
                        if self.game_state == "get_ready":
                            self.game_state = "playing"
                            self.pipes.append(Pipe(WIN_WIDTH + 50))
                        elif self.bird.alive and self.game_state == "playing":
                            self.bird.flap()
                        elif self.game_state == "game_over":
                            self.reset_round()

            self.update()
            self.draw()

        
