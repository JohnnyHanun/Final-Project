import pygame
import pygame_gui
from Utils import Utils
from pygame.locals import (
    RLEACCEL,
    QUIT,
)
"""CONSTANTS"""
NODE_R = 30
Utils = Utils()
NODE_NAME = Utils.gen_letters()


class Node(pygame.sprite.Sprite):
    def __init__(self,
                 center: tuple[int, int],
                 radius=NODE_R):
        super(Node, self).__init__()
        self.center = center
        self.surf = pygame.Surface((2 * NODE_R, 2 * NODE_R))
        pygame.draw.circle(self.surf, 'Green', (NODE_R, NODE_R), NODE_R)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=self.center)
        self.text_view = pygame.font.SysFont("arial", 15, True, True).render(next(NODE_NAME), True, (0, 0, 0))



