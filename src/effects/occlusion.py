# -*- coding: utf-8 -*-

from utils.resourcesmanager import ResourcesManager


class Occlude:
    """
    Class to draw a black image on the surface to reduce the vision of the player
    """

    def __init__(self):
        self.image = ResourcesManager.loadImage('occlude_vision.png', transparency=True)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
