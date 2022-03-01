# -*- coding: utf-8 -*-

from game.director import Director
from game.interactive import Interactive
from player.entity import Entity


class Object(Interactive, Entity):
    """
    Any type of object, which interacts by collisions and whose position needs to be updated with respect to the player
    """

    def __init__(self, image, collisionsGroup, position, player, name=None):
        Interactive.__init__(self, image, collisionsGroup, position, name)
        Entity.__init__(self, player, position)

    def remove(self):
        """
        Removes the object from all the groups of the scene, so it disappears completely
        """

        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "objectsGroup")
        scene.removeFromGroup(self, "objectsToEvent")
        scene.removeFromGroup(self, "objectsToUpdate")
        scene.removeFromGroup(self, "foregroundGroup")
        scene.removeFromGroup(self, "uiGroup")

        self._player.detach(self)


class InstaUseObject(Object):
    """
    Object whose effect is executed exactly when the player picked it up
    """

    def __init__(self, image, playerGroup, callbacks, position, name=None):
        super().__init__(image, [playerGroup], position, playerGroup.sprites()[0], name)
        self.callbacks = callbacks  # functions executed onCollisionEnter with the player

    def onCollisionEnter(self, collided):

        for callback in self.callbacks:
            callback()

        self.remove()
