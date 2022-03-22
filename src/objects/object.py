# -*- coding: utf-8 -*-

import pygame

from game.director import Director
from game.interactive import Interactive
from game.entity import Entity
from utils.resourcesmanager import ResourcesManager


class Object(pygame.sprite.Sprite, Entity, Interactive):
    """
    Any type of object, which interacts by collisions and whose position needs to be updated with respect to the player
    """

    def __init__(self, image, position, playerGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = ResourcesManager.loadImage(image, transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = position

        Entity.__init__(self, position)
        Entity.setPlayer(self, playerGroup.sprites()[0])

        Interactive.__init__(self, self.rect)
        self.addCollisionGroup(playerGroup)

    def update(self, *args):
        pygame.sprite.Sprite.update(self, *args)
        self.updateCollisions(self, *args)

    def activate(self):
        super().activate()
        Director().getCurrentScene().addToGroup(self, "objectsGroup")

    def deactivate(self):
        super().deactivate()
        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "objectsGroup")
        scene.removeFromGroup(self, "objectsToEvent")
        scene.removeFromGroup(self, "foregroundGroup")
        scene.removeFromGroup(self, "uiGroup")


class InstaUseObject(Object):
    """
    Object whose effect is executed exactly when the player picked it up
    """

    def __init__(self, image, playerGroup, callbacks, position):
        super().__init__(image, position, playerGroup)
        self.callbacks = callbacks  # functions executed onCollisionEnter with the player

    def onCollisionEnter(self, collided):
        for callback in self.callbacks:
            callback()

        self.deactivate()
