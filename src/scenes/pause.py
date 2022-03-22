# -*- coding: utf-8 -*-
import sys

import pygame
from pygame.locals import *

from game.dialogue import TextUI
from game.director import Director
from scenes.scene import Scene


class PauseScene(Scene):

    def __init__(self):
        super().__init__()
        self.isDrew = False

    def events(self, events):

        for event in events:

            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Unpause the game
            elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_p):
                Director().pop()
                Director().getCurrentScene().player.eventsEnabled = True

    def update(self, *args):
        pass

    def draw(self, surface):

        if not self.isDrew:
            self.isDrew = True  # apply the opacity once, so the previous scene is still visible

            # Create a transparent surface of the same size of the window
            transparentSurface = pygame.Surface((800, 600), pygame.SRCALPHA)
            transparentSurface.fill((0, 0, 0, 200))  # fill the transparent surface with a black color
            surface.blit(transparentSurface, (0, 0))  # draw on the surface

            text = TextUI('munro.ttf', 60, (400, 300), (255, 255, 255))
            text.setText("Press 'p' to resume...")
            text.draw(surface)

    def onEnterScene(self):
        pass

    def onExitScene(self):
        pass