import pygame
from settings import *

font = pygame.font.Font(None, 30)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, value):
        super().__init__(groups)
        self.value = value
        self.text_surf = font.render(f'{self.value}', True, 'Black')
        self.text_rect = self.text_surf.get_rect(center=pos/2)
        self.rect = pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)
        self.text_rect.center = self.rect.center
        pygame.draw.rect(self.text_surf, 'Black', self.text_rect)
        self.rect = pygame.draw.rect(self.screen, COLORS[value], self.rect, border_radius=8)

