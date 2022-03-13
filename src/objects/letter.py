# -*- coding: utf-8 -*-

from pygame.locals import *

from game.dialogue import TextUI
from game.director import Director
from objects.door import Switch

from utils.resourcesmanager import ResourcesManager


class Letter(Switch):
    """
    Object with a message to the player
    """

    def __init__(self, position, playerGroup, digit):
        Switch.__init__(self, "closed_letter.png", position, playerGroup, [], lock=False, active=True)

        self._opened = False  # if the player has collided with it
        self.id = id  # image file of the letter opened

        self.digit = TextUI("southernaire.ttf", 200, (400, 250), (0, 0, 0))
        self.digit.setText(str(digit))

    def onCollisionEnter(self, collided):

        if self._opened:
            return

        super().onCollisionEnter(collided)
        self.open()

    def open(self):
        """
        Changes the sprite from the closed to the opened state, disables the events from the player and starts
        to catch them itself.
        """

        self.position = (400, 300)

        self.image = ResourcesManager.loadImage(f"letter_opened.png", transparency=True)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self._opened = True
        ResourcesManager.loadSound("turn_page.wav").play()

        # Change group to the foreground one, so it is always visible
        scene = Director().getCurrentScene()

        self._player.stop()

        scene.removeFromGroup(self, "objectsGroup")
        scene.addToGroup(self, "foregroundGroup")
        scene.addToGroup(self.digit, "uiGroup")
        scene.addToGroup(self, "objectsToEvent")


    def close(self):
        """
        Removes the object from the scene, returning the events to the player
        """

        self._opened = False

        scene = Director().getCurrentScene()
        scene.removeFromGroup(self.digit, "uiGroup")
        self._player.eventsEnabled = True

        self.deactivate()
        self.notify()

    def events(self, events):

        for event in events:

            if event.type == KEYDOWN and event.key == K_SPACE:
                self.close()

