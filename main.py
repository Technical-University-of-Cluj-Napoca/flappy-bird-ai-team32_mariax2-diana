import pygame
from settings import *
from game import Game 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    while True:
        screen.fill((140, 200, 255))

        title = font.render("Flappy Bird", True, (0, 0, 0))
        manual_text = font.render("1- Manual Mode (SPACE)", True, (0, 0, 0))
        quit_text = font.render("ESC- Quit", True, (0, 0, 0))

        screen.blit(title, (50, 80))
        screen.blit(manual_text, (50, 200))
        screen.blit(quit_text, (50, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game = Game() 
                    game.run()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        clock.tick(60)

if __name__ == "__main__":
    main()
