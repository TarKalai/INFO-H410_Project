from settings import *
from debug import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, value=0):
        """
        Creates a Tile to bea displayed on the screen.
        :param pos: (Int, Int) a tuple corresponding to the (x, y) coordinates the tiles must be on the screen.
        :param groups: (List of Sprite) the group of sprite the tile belongs to.
        :param value: (Int) The value inside the Tile.
        """
        super().__init__(groups)

        self.value = value
        self.posX, self.posY = pos

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
