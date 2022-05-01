import pygame

pygame.init()
font = pygame.font.Font(None, 40)


def debug(info, y=10, x=10):
    """
    Used for debugging purpose. It displays a small black box with the information given by argument at the (x, y)
    coordinates of the screen.
    :param info: (String) the information to display
    :param y: (Int) y coordinate
    :param x: (Int) x coordinate
    :return: None
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)
