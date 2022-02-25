# -*- coding: utf-8 -*-

from objects.interactive import InstaUseObject

class LabCoat(InstaUseObject):
    """
    Object that increases the speed of the player when it is picked up
    """

    def __init__(self, playerGroup, phase, position=(0, 0)):
        player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        super().__init__("labCoat.png", playerGroup, player.increaseSpeed, phase, position=position)
