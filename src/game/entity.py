# -*- encoding: utf-8 -*-
from characters.character import Player
from game.director import Director
from utils.observer import Observer


class Entity(Observer):
    """
    Every object with a position in the world must inherit from this class, to update its position with respect to
    the player position, since the camera is frozen and it is the world who moves
    """

    def __init__(self, position):
        Observer.__init__(self)

        self._lastPlayerPos = None
        self.position = position
        self.offset = (0, 0)  # difference between the last position and the current position of the player

    def setPlayer(self, player):
        player.attach(self)
        self._lastPlayerPos = player.getPos()

    def updateObserver(self, subject):

        if type(subject) == Player:
            # Calculate the scroll given by the difference in the position of the player and substract it from
            # the our position (if the player goes to the right, the entities go the left)
            playerPos = subject.getPos()
            self.offset = playerPos[0] - self._lastPlayerPos[0], playerPos[1] - self._lastPlayerPos[1]

            self.position = self.position[0] - self.offset[0], self.position[1] - self.offset[1]
            self._lastPlayerPos = playerPos

            if hasattr(self, "rect"):
                self.rect.center = self.position

    def activate(self):
        scene = Director().getCurrentScene()
        scene.addToGroup(self, "objectsToUpdate")

    def deactivate(self):
        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "objectsToUpdate")
        scene.player.detach(self)
