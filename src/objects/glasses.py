# -*- coding: utf-8 -*-

from objects.object import InstaUseObject

from utils.observer import Subject, Observer
from utils.resourcesmanager import ResourcesManager


class Glasses(InstaUseObject, Subject):
    """
    Object that increases the sight of the player when it is picked up
    """

    def __init__(self, playerGroup, position):
        Subject.__init__(self)
        InstaUseObject.__init__(self, "glasses.png", playerGroup, [self.playSound], position)

    def onCollisionEnter(self, collided):
        super().onCollisionEnter(collided)
        self.notify()

    def playSound(self):
        ResourcesManager.loadSound("pick_object.wav").play()
