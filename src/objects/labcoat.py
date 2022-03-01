# -*- coding: utf-8 -*-

from objects.object import InstaUseObject
from utils.resourcesmanager import ResourcesManager


class LabCoat(InstaUseObject):
    """
    Object that increases the speed of the player when it is picked up
    """

    def __init__(self, playerGroup, position):
        player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        super().__init__("labCoat.png", playerGroup, [player.increaseSpeed, self.playSound], position)

    def playSound(self):
        ResourcesManager.loadSound("leather_inventory.wav").play()
