# -*- coding: utf-8 -*-
import pygame

from characters.personaje2 import Player
from game.director import Director
from objects.letter import Letter
from objects.object import Object

from utils.observer import Subject, Observer
from utils.resourcesmanager import ResourcesManager


class Switch(Object, Subject):

    def __init__(self, position, playerGroup, room=None):
        Object.__init__(self, "white_tile.jpg", position, playerGroup)
        Subject.__init__(self)

    def onCollisionEnter(self, collided):
        self.notify()
        self.remove()

class SwitchOut(Object, Subject):

    def __init__(self, position, playerGroup, room=None):
        super().__init__( "white_tile.jpg", position, playerGroup)
        Subject.__init__(self)
        self.room = room
        self.active = False
        
    def updateObserver(self, subject):
        Object.updateObserver(self, subject)
        print(isinstance(subject, Switch))
        if isinstance(subject, Switch):
            self.active = True

    def onCollisionEnter(self, collided):
       if self.active:
            self.remove()
            self.notify()



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
            self._locked = True
            self.close()
        elif isinstance(subject, Letter):
            self._locked = False
            self.open()
        elif isinstance(subject, SwitchOut):
            self._locked = True
            self.close()


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
