# -*- coding: utf-8 -*-

from objects.interactive import InstaUseObject
from utils.resourcesmanager import ResourcesManager


class Glasses(InstaUseObject):
    """
    Object that increases the sight of the player when it is picked up
    """

    def __init__(self, playerGroup, position=(0, 0)):
        player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        super().__init__("glasses.png", playerGroup, [player.addGlasses, self.playSound], position=position)

    def playSound(self):
        ResourcesManager.loadSound("pick_object.wav").play()
