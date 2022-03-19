import pygame
from settings import *
from debug import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, value=0):
        super().__init__(groups)

        self.value = value
        self.posX, self.posY = pos
        self.targetPosX, self.targetPosY = pos
        # creating the surface tile
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # filing the surface with a color depending on the value
        self.image.fill(COLORS[value])

        if value:
            # creating text that will be inside the surface
            self.font = pygame.font.SysFont('Arial', 40, bold=1)
            self.text_surf = self.font.render(f'{self.value}', True, 'Black')
            self.text_rect = self.text_surf.get_rect(center=(TILESIZE / 2, TILESIZE / 2))

            # adding the text to the surface
            self.image.blit(self.text_surf, self.text_rect)

        self.direction = pygame.math.Vector2()
        self.speed = SPEED

    def move(self, speed):
        self.rect.center += self.direction * speed
        self.posX += self.direction[0] * speed
        self.posY += self.direction[1] * speed

    def set_direction(self, direction):
        self.direction = direction

    def finished_movement(self):
        """
            Tell if the movement is finished or not. 
        """
        if self.posX == self.targetPosX and self.posY == self.targetPosY:
            self.set_direction(pygame.math.Vector2())
        return self.posX == self.targetPosX and self.posY == self.targetPosY

    def update_value(self, value):
        self.value = value
        self.image.fill(COLORS[self.value])
        self.text_surf = self.font.render(f'{self.value}', True, 'Black')
        self.text_rect = self.text_surf.get_rect(center=(TILESIZE / 2, TILESIZE / 2))
        self.image.blit(self.text_surf, self.text_rect)

    def new_target(self, direction):
        self.targetPosX = self.targetPosX + TILEDISPLACEMENT * direction[0]
        self.targetPosY = self.targetPosY + TILEDISPLACEMENT * direction[1]

    def update(self):
        self.move(self.speed)
        debug(str(self.posX) + " " + str(self.targetPosX))
