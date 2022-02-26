# -*- coding: utf-8 -*-

import pygame.mouse
import pygame_menu

from menu.menu import Menu
from menu.conf import ConfMenu

from phase.test import PhaseTest

from utils.resourcesmanager import ResourcesManager


class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self, director):
        super().__init__(director, "Main menu")

        self._menu.add.button('Play', self.onStartGame)  # button to start the game
        self._menu.add.button('Configuration', self.onOpenConfigurationMenu)  # button to edit the configuration
        self._menu.add.button('Quit', pygame_menu.events.EXIT)  # button to exit the game

        self._startGame = False  # flag to know when to stop the main menu music
        ResourcesManager.loadMusic("main_menu.mp3")
        pygame.mixer.music.play()

    def onEnterScene(self):
        super().onEnterScene()

        if self._startGame:
            self._startGame = False
            ResourcesManager.loadMusic("main_menu.mp3")
            pygame.mixer.music.play(-1)

    def onExitScene(self):
        super().onExitScene()

        if self._startGame:
            pygame.mixer.music.stop()

    def onStartGame(self):
        """
        Initiate the game
        """

        self._startGame = True
        phase1 = PhaseTest(self._director)
        self._director.push(phase1)

    def onOpenConfigurationMenu(self):
        """
        Edit the configuration of the game
        """

        confMenu = ConfMenu(self._director)
        self._director.push(confMenu)
