# -*- coding: utf-8 -*-

from objects.interactive import InstaUseObject

class Glasses(InstaUseObject):
    """
    Object that increases the sight of the player when it is picked up
    """

    def __init__(self, playerGroup, phase, position=(0, 0)):
        player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        super().__init__("glasses.png", playerGroup, player.addGlasses, phase, position=position)
