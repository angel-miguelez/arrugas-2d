# -*- coding: utf-8 -*-

import pygame

from objects.object import Object

from utils.observer import Subject
from utils.resourcesmanager import ResourcesManager


class Switch(Object, Subject):
    """
    Object to lock or unlock another object
    """

    def __init__(self, image, position, playerGroup, entitiesToUpdate, lock=True, visible=True, active=True, spawnEntities=False):
        Object.__init__(self, image, position, playerGroup)
        Subject.__init__(self)

        self.lock = lock  # if the switch must lock or unlock something
        self.activated = False  # if it has switched the state

        self.visible = visible  # if it is visible (the player cannot step over it)
        self.active = active  # if the lock effect is active

        # If entitiesToUpdate is not empty, and spawnEntities is False, then those entities are removed
        # If entitiesToUpdate is not empty, and spawnEntities is True, then those entities are activated
        self.entities = entitiesToUpdate
        self.spawnEntities = spawnEntities

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

        # Activate or deactivate the entities attached to it
        for entity in self.entities:
            if self.spawnEntities:
                entity.activate()
            else:
                entity.deactivate()

        self.notify()

    def updateObserver(self, subject):
        Object.updateObserver(self, subject)

        if isinstance(subject, Switch):
            self.active = True


class Door(Object):
    """
    Object that allows the player to enter a specific room or blocks it from leaving it.
    """

    def __init__(self, position, playerGroup, room=None):
        super().__init__("door_closed.png", position, playerGroup)

        self.room = room
        self._locked = False  # True to block the player (activate collisions)
        self._opened = False

    def onCollisionEnter(self, collided):

        if self._opened:
            return

        # If the player can enter the room (not visited yet)
        if not self._locked:
            self.open()

        # If the door is blocked, the player cannot go through it (room visited previously or still inside it)
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
        self._opened = True
        self.image = ResourcesManager.loadImage("door_opened.png", transparency=True)
        ResourcesManager.loadSound("door.wav").play()

    def close(self):
        self._opened = False
        self.image = ResourcesManager.loadImage("door_closed.png", transparency=True)
        ResourcesManager.loadSound("door.wav").play()
