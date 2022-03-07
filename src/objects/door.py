# -*- coding: utf-8 -*-
import pygame

from characters.character import Player
from objects.object import Object

from utils.observer import Subject
from utils.resourcesmanager import ResourcesManager


class Switch(Object, Subject):

    def __init__(self, image, position, playerGroup, lock=True, visible=True, active=True):
        Object.__init__(self, image, position, playerGroup)
        Subject.__init__(self)

        self.lock = lock  # if the switch must lock or unlock something
        self.activated = False  # if it has switched the state

        self.visible = visible  # if it is visible (detect collisions)
        self.active = active  # if the lock effect is active

    def onCollisionEnter(self, collided):

        # If is visible, then the player can collide with it
        if self.visible:
            collided.x, collided.y = collided.lastPos
            self.objectsEnterCollision.remove(collided)

        # If it is not active or has been activated, it has no effect
        if self.activated or not self.active:
            return

        self.activated = True
        self.image = pygame.transform.flip(self.image, True, False)
        self.notify()

    def updateObserver(self, subject):
        Object.updateObserver(self, subject)

        if isinstance(subject, Switch):
            self.active = True


class Door(Object):

    def __init__(self, position, playerGroup, room=None):
        super().__init__("door_closed.png", position, playerGroup)

        self.room = room
        self._locked = False
        self._opened = False

    def onCollisionEnter(self, collided):

        if not self._locked:
            self.open()
        else:
            collided.x, collided.y = collided.lastPos
            self.objectsEnterCollision.remove(collided)

    def updateObserver(self, subject):
        Object.updateObserver(self, subject)

        if isinstance(subject, Switch):
            self._locked = subject.lock
            if subject.lock:
                self.close()
            else:
                self.open()

    def open(self):

        if self._opened:
            return

        self._opened = True
        self.image = ResourcesManager.loadImage("door_opened.png", transparency=True)
        ResourcesManager.loadSound("door.wav").play()

    def close(self):

        if not self._opened:
            return

        self._opened = False
        self.image = ResourcesManager.loadImage("door_closed.png", transparency=True)
        ResourcesManager.loadSound("door.wav").play()
