import pygame
from settings import *
from game import Game 
from button import Button 

current_high_score = 0

def start_manual():
    global current_high_score
    game = Game(mode="manual", high_score_in=current_high_score)
    current_high_score = game.run()

def start_auto():
    global current_high_score
    game = Game(mode="auto", high_score_in=current_high_score)
    current_high_score = game.run()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bg = pygame.transform.scale(
        pygame.image.load("background2.png").convert(),
        (WIN_WIDTH, WIN_HEIGHT)
        ) 
    logo = pygame.transform.scale(
        pygame.image.load("logo.png").convert_alpha(),
        (200, 200)
    )
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    btn_manual = Button(
        x=WIN_WIDTH//2 - 130,
        y=260,
        width=260,
        height=50,
        text="Manual Mode",
        font=font,
        callback=start_manual
    )

    btn_auto = Button(
        x=WIN_WIDTH//2 - 130,
        y=330,
        width=260,
        height=50,
        text="Auto Mode",
        font=font,
        callback=start_auto
    )

    while True:
        screen.blit(bg, (0, 0))
        logo_x = WIN_WIDTH // 2 - logo.get_width() // 2
        logo_y = 50
        screen.blit(logo, (logo_x, logo_y))

        btn_manual.draw(screen)
        btn_auto.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            btn_manual.handle_event(event)
            btn_auto.handle_event(event)

        clock.tick(60)

if __name__ == "__main__":
    main()
