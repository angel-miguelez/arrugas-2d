# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import pygame
from pygame.locals import *

from conf.configuration import ConfManager
from game.scene import Scene
from game.level import Level
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

        self.level = Level(basic_layout, NULL)  # Setup level structure

        self.x, self.y = (400, 400)
        self.speedX, self.speedY = 5, 5

    def events(self, events):

        for event in events:

            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("[Phase1] Finishing phase1")
                self._director.pop()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[self.MOVE_UP]:
            self.y -= self.speedY
        elif keys_pressed[self.MOVE_DOWN]:
            self.y += self.speedY
        elif keys_pressed[self.MOVE_RIGHT]:
            self.x += self.speedX
        elif keys_pressed[self.MOVE_LEFT]:
            self.x -= self.speedX


    def update(self, time):
        pass

    def draw(self, surface):
        surface.fill((0, 0, 0)) #Background color

        self.level.setSurface(surface)
        self.level.run() #Draw the level

        #Player with movement
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), 4, 0)
