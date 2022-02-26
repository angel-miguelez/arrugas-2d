# -*- coding: utf-8 -*-

import pygame

from conf.configuration import ConfManager

from game.scene import Scene


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

    def onEnterScene(self):
        pygame.mouse.set_visible(False)

    def onExitScene(self):
        pass
