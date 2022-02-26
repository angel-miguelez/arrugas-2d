# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from effects.occlusion import Occlude

from map.level import Level

from phase.phase import Phase

from player.personaje2 import Player

from objects.glasses import Glasses
from objects.labcoat import LabCoat

from res.levels import *


class PhaseTest(Phase):
    """
    Fase usada para probar cosas
    """

    def __init__(self, director):
        super().__init__(director, "PhaseTest")

        # Level
        self.level = Level(basic_layout)  # Setup map structure

        # Player
        self.player = Player()
        self.playerGroup = pygame.sprite.Group(self.player)

        # Objects
        self.glasses = Glasses(self.playerGroup, position=(300, 300))
        self.labcoat = LabCoat(self.playerGroup, position=(400, 400))
        self.objectsGroup = pygame.sprite.Group(self.glasses, self.labcoat)

        # Effects
        self.occlude = Occlude()

    def events(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._director.pop()

        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed, self.MOVE_UP, self.MOVE_DOWN, self.MOVE_LEFT, self.MOVE_RIGHT)

    def update(self, time):
        self.playerGroup.update(time)
        self.objectsGroup.update(time)

    def draw(self, surface):
        surface.fill((0, 0, 0))  # Background color

        self.level.run(surface)  # Draw the map

        self.objectsGroup.draw(surface)
        self.playerGroup.draw(surface)

        if not self.player.hasGlasses:
            self.occlude.draw(surface)

    def onEnterScene(self):
        super().onEnterScene()
        self.playMusic("phase1_background.ogg", "sound.game_music_volume")

    def onExitScene(self):
        super().onExitScene()
        pygame.mixer.music.stop()

    def removeFromGroup(self, object, groupName):

        if groupName == "objects":
            self.objectsGroup.remove(object)
