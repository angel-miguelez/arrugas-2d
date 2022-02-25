# -*- coding: utf-8 -*-

from player.gestorRecursos import GestorRecursos


class Occlude:
    """
    Class to draw a black image on the surface to reduce the vision of the player
    """

    def __init__(self):
        self.image = GestorRecursos.CargarImagen('occludeVision.png', transparency=True)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
