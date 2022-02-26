# -*- coding: utf-8 -*-

from objects.interactive import InstaUseObject

from utils.observer import Subject, Observer
from utils.resourcesmanager import ResourcesManager

class Glasses(InstaUseObject, Subject):
    """
    Object that increases the sight of the player when it is picked up
    """

    __observers = []

    def __init__(self, playerGroup, position=(0, 0)):
        player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        super().__init__("glasses.png", playerGroup, [player.addGlasses, self.playSound], position=position)

    def onCollisionEnter(self, collided):
        super().onCollisionEnter(collided)
        self.notify()

    def attach(self, observer: Observer):
        self.__observers.append(observer)

    def detach(self, observer: Observer):
        self.__observers.remove(observer)

    def notify(self):
        for observer in self.__observers:
            observer.update(self)

    def playSound(self):
        ResourcesManager.loadSound("pick_object.wav").play()
