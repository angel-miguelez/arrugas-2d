# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from conf.configuration import ConfManager

from game.director import Director
from game.scene import Scene


class Phase(Scene):
    """
    Base class to every playable scene
    """

    def __init__(self, director, name):
        super().__init__(director, name)

        self._conf = ConfManager()

        # Load the player bindings
        self.MOVE_UP, self.MOVE_DOWN, self.MOVE_RIGHT, self.MOVE_LEFT = self._conf.getPlayerMovementBinds()

        self.level = None  # zone where the player can move
        self.player = None

        # All the groups we have, each of them with some different behaviour
        self.backgroundGroup = pygame.sprite.Group()  # background images or effects
        self.playerGroup = pygame.sprite.Group()
        self.npcGroup = pygame.sprite.Group()
        self.objectsGroup = pygame.sprite.Group()
        self.foregroundGroup = pygame.sprite.Group()  # e.g. visual effects (occlusion)
        self.uiGroup = []  # UI elements do not need to be sprites, they can be simple images or text

        self.objectsToEvent = []  # objects that need to catch events
        self.objectsToUpdate = []  # objects that need to be updated

    def onEnterScene(self):
        pygame.mouse.set_visible(False)

    def onExitScene(self):
        pass

    def events(self, events):

        for event in events:

            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Return to the previous scene
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                Director().pop()

        # Update the player movement
        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed, self.MOVE_UP, self.MOVE_DOWN, self.MOVE_LEFT, self.MOVE_RIGHT)

        # Update every object that need to catch events
        for object in self.objectsToEvent:
            object.events(events)

    def update(self, *args):

        for object in self.objectsToUpdate:
            object.update(*args)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        self.backgroundGroup.draw(surface)
        self.level.draw(surface)

        self.objectsGroup.draw(surface)

        self.npcGroup.draw(surface)
        self.playerGroup.draw(surface)

        self.foregroundGroup.draw(surface)

        for ui in self.uiGroup:
            ui.draw(surface)
