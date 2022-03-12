# -*- coding: utf-8 -*-

import pygame

from game.director import Director
from utils.observer import Observer, Subject
from utils.resourcesmanager import ResourcesManager


class Occlude(pygame.sprite.Sprite, Observer):
    """
    Class to draw a black image on the surface to reduce the vision of the player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ResourcesManager.loadImage('occlude_vision.png', transparency=True)
        self.rect = self.image.get_rect()

    def updateObserver(self, subject: Subject) -> None:
        self.image = ResourcesManager.loadImage('occlude_vision2.png', transparency=True)
        self.rect = self.image.get_rect()
        #Director().getCurrentScene().removeFromGroup(self, "foregroundGroup")
