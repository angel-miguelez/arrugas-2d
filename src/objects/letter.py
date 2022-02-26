# -*- coding: utf-8 -*-

from pygame.locals import *

from game.director import Director

from objects.interactive import Interactive

from utils.resourcesmanager import ResourcesManager


class Letter(Interactive):
    """
    Object with a message to the player
    """

    def __init__(self, playerGroup, id="01", position=(0, 0)):
        super().__init__("closed_letter.png", [playerGroup], position=position)

        self._player = playerGroup.sprites()[0]  # since playerGroup is a group with just the player
        self._opened = False  # if the player has collided with it

        self.id = id

    def onCollisionEnter(self, collided):
        ResourcesManager.loadSound("turn_page.wav").play()
        self._player.disableEvents()  # so the player has to close the letter before moving again
        self.open()

    def open(self):
        """
        Changes the sprite from the closed to the opened state, disables the events from the player and starts
        to catch them itself.
        """

        self._initializeSprite(f"letter{self.id}.png", (225, 500))
        self._opened = True

        # Change to group to the foreground one, so it is always visible
        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "objectsGroup")
        scene.addToGroup(self, "foregroundGroup")

    def close(self):
        """
        Removes the object from the scene, returning the events to the player
        """

        scene = Director().getCurrentScene()
        scene.removeFromGroup(self, "foregroundGroup")

    def events(self, events):

        # Only get events when it is opened
        if not self._opened:
            return

        for event in events:

            # When pressing any key, close the letter
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._player.enableEvents()
                self.close()
