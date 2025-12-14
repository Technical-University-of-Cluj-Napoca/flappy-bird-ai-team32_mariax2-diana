import pygame
from settings import WHITE

class Button:
    def __init__(self, x, y, width, height, text, font, callback, bg_color=(240, 150, 180), hover_color=(247, 182, 200), 
                border_radius=10, border_color=(0, 0, 0), border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_radius = border_radius 
        self.border_color = border_color 
        self.border_width = border_width
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.callback()