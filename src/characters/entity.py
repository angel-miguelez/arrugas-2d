# -*- encoding: utf-8 -*-

#from characters.personaje2 import Player
from utils.observer import Observer


class Entity(Observer):
    """
    Every object with a position in the world must inherit from this class, to update its position with respect to
    the player position, since the camera is frozen and it is the world who moves
    """

    def __init__(self, position):
        self._player = None
        self._lastPlayerPos = None
        self.position = position
        self.offset = None

    def setPlayer(self, player):
        Observer.__init__(self)

        self._player = player
        self._player.attach(self)

        self._lastPlayerPos = self._player.getPos()
        self.offset = (0, 0)

    def updateObserver(self, subject):

        playerPos = self._player.getPos()
        self.offset = playerPos[0] - self._lastPlayerPos[0], playerPos[1] - self._lastPlayerPos[1]

        self.position = self.position[0] - self.offset[0], self.position[1] - self.offset[1]
        self._lastPlayerPos = playerPos

        if hasattr(self, "rect"):
            self.rect.center = self.position
