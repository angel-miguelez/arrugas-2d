import pygame

class Tile(pygame.sprite.Sprite):

    """
        Tile class allows us to setup the neccessary information to draw and update a tile on the screen
    """

    def __init__(self, pos, size, color):
        super().__init__()
        #Setup shape and color for the Tile
        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        #Set the position of the Tile
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, xshift, yshift):

        """
            Update method to simulate movement on the map
        """
        self.rect.x += (xshift * 2)
        self.rect.y += (yshift * 2)