import pygame
from settings import *
from game import Game 
from button import Button 

manual_high_score = 0
auto_high_score = 0
show_scores = False
def load_scores():
    try:
        with open("scores.txt", "r") as f:
            lines = f.readlines()
            manual = int(lines[0].split(":")[1])
            auto = int(lines[1].split(":")[1])
            return manual, auto
    except:
        return 0, 0
    
def save_scores(manual, auto):
    with open("scores.txt", "w") as f:
        f.write(f"manual:{manual}\n")
        f.write(f"auto:{auto}\n")

def open_scores():
    global show_scores
    show_scores = True

def start_manual():
    global manual_high_score
    game = Game(mode="manual", high_score_in=manual_high_score)
    score = game.run()
    manual_high_score = max(manual_high_score, score)
    save_scores(manual_high_score, auto_high_score)

def start_auto():
    global auto_high_score
    game = Game(mode="auto", high_score_in=auto_high_score)
    score = game.run()
    auto_high_score = max(auto_high_score, score)
    save_scores(manual_high_score, auto_high_score)

def main():
    global manual_high_score, auto_high_score, show_scores
    manual_high_score, auto_high_score = load_scores()
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

    btn_scores = Button(
        x=WIN_WIDTH//2 - 130,
        y=400,
        width=260,
        height=50,
        text="HIGH SCORES",
        font=font,
        callback=open_scores
    )

    while True:
        screen.blit(bg, (0, 0))
        logo_x = WIN_WIDTH // 2 - logo.get_width() // 2
        logo_y = 50
        screen.blit(logo, (logo_x, logo_y))

        btn_manual.draw(screen)
        btn_auto.draw(screen)
        btn_scores.draw(screen)

        if show_scores:
            card = pygame.Rect(
                WIN_WIDTH//2 - 150,
                WIN_HEIGHT//2 - 150,
                300,
                300
            )

            pygame.draw.rect(screen, (255,255,255), card, border_radius=10)
            pygame.draw.rect(screen, (0,0,0), card, 4, border_radius=10)

            title = font.render("HIGH SCORES", True, (0,0,0))
            screen.blit(title, title.get_rect(center=(WIN_WIDTH//2, card.top + 40)))

            manual = font.render(f"Manual: {manual_high_score}", True, (0,0,0))
            auto = font.render(f"Auto: {auto_high_score}", True, (0,0,0))

            screen.blit(manual, manual.get_rect(center=(WIN_WIDTH//2, card.top + 120)))
            screen.blit(auto, auto.get_rect(center=(WIN_WIDTH//2, card.top + 170)))

            hint = font.render("ESC to close", True, (100,100,100))
            screen.blit(hint, hint.get_rect(center=(WIN_WIDTH//2, card.bottom - 30)))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            btn_manual.handle_event(event)
            btn_auto.handle_event(event)
            btn_scores.handle_event(event)
            if show_scores:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    show_scores = False

        clock.tick(60)

if __name__ == "__main__":
    main()
