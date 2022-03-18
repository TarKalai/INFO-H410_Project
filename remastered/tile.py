import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, value=0):
        super().__init__(groups)

        self.value = value

        # creating the surface tile
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # filing the surface with a color depending on the value
        self.image.fill(COLORS[value])

        if value:
            # creating text that will be inside the surface
            self.font = pygame.font.SysFont('Arial', 40, bold=1)
            self.text_surf = self.font.render(f'{self.value}', True, 'Black')
            self.text_rect = self.text_surf.get_rect(center=(TILESIZE/2, TILESIZE/2))

            # adding the text to the surface
            self.image.blit(self.text_surf, self.text_rect)

        self.direction = pygame.math.Vector2()
        self.speed = SPEED

    def move(self, speed):
        self.rect.center += self.direction * speed

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.move(self.speed)


