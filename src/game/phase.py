# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys

from conf.configuration import ConfManager

from effects.occlusion import Occlude

from game.scene import Scene
from game.level import Level

from player.personaje2 import Player

from objects.glasses import Glasses
from objects.labcoat import LabCoat

from res.levels import *


class Phase(Scene):
    """
    Base class to every playable scene
    """

    def __init__(self, director, name):
        super().__init__(director, name)

        self._conf = ConfManager()

        self.MOVE_UP = self._conf.getBind("player.movement.up")
        self.MOVE_DOWN = self._conf.getBind("player.movement.down")
        self.MOVE_RIGHT = self._conf.getBind("player.movement.right")
        self.MOVE_LEFT = self._conf.getBind("player.movement.left")

    def onEnter(self):
        pygame.mouse.set_visible(False)

    def onExit(self):
        pass


class PhaseTest(Phase):
    """
    Fase usada para probar cosas
    """

    def __init__(self, director):
        super().__init__(director, "PhaseTest")

        # Level
        self.level = Level(basic_layout, None)  # Setup level structure

        # Player
        # self.x, self.y = (400, 400)
        # self.speedX, self.speedY = 5, 5
        self.player = Player()
        self.playerGroup = pygame.sprite.Group(self.player)

        # Objects
        self.glasses = Glasses(self.playerGroup, self, position=(300, 300))
        self.labcoat = LabCoat(self.playerGroup, self, position=(400, 400))
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
        surface.fill((0, 0, 0)) #Background color

        self.level.setSurface(surface)
        self.level.run() #Draw the level

        self.objectsGroup.draw(surface)
        self.playerGroup.draw(surface)

        if not self.player.hasGlasses:
            self.occlude.draw(surface)

    def removeFromGroup(self, object, groupName):

        if groupName == "objects":
            self.objectsGroup.remove(object)
