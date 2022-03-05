# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from game.director import Director
from game.scene import Scene


class CinematicPhase(Scene):
    """
    Base class to every non-playable scene (typically dialogues)
    """

    def __init__(self):

        super().__init__()

        # All the groups we have, each of them with some different behaviour
        self.backgroundImage = None
        self.backgroundGroup = pygame.sprite.Group()  # background images or effects
        self.foregroundGroup = pygame.sprite.Group()  # e.g. visual effects (occlusion)
        self.uiGroup = []  # UI elements do not need to be sprites, they can be simple images or text

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

        for object in self.objectsToEvent:
            object.events(events)

    def update(self, *args):

        for object in self.objectsToUpdate:
            object.update(*args)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        surface.blit(self.backgroundImage, (0, 0))
        self.backgroundGroup.draw(surface)
        self.foregroundGroup.draw(surface)

        for ui in self.uiGroup:
            ui.draw(surface)
