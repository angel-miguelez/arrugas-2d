# -*- encoding: utf-8 -*-

from utils.observer import Observer


class Entity(Observer):
    """
    Every object with a position in the world must inherit from this class, to update its position with respect to
    the player position, since the camera is frozen and it is the world who moves
    """

    def __init__(self):
        self._player = None
        self._lastPlayerPos = None
        self.position = None

    def setPlayer(self, player, position):
        Observer.__init__(self)

        self._player = player
        self._player.attach(self)

        self._lastPlayerPos = self._player.getPos()
        self.position = position  # position in the world

    def updateObserver(self, subject):

        if self._player is None:
            return

        playerPos = self._player.getPos()
        offset = playerPos[0] - self._lastPlayerPos[0], playerPos[1] - self._lastPlayerPos[1]

        self.position = self.position[0] - offset[0], self.position[1] - offset[1]
        self._lastPlayerPos = playerPos

        if hasattr(self, "rect"):
            self.rect.center = self.position
