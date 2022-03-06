# -*- coding: utf-8 -*-

import pygame.mouse
import pygame_menu

from game.director import Director
from menu.settings import SettingsMenu
from menu.menu import Menu

from phase.test import PhaseTest


class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self):
        super().__init__("Arrugas")

        self._menu.add.button('Play', self.onStartGame)  # button to start the game
        self._menu.add.button('Configuration', self.onOpenConfigurationMenu)  # button to edit the configuration
        self._menu.add.button('Quit', pygame_menu.events.EXIT)  # button to exit the game

        self._startGame = False  # flag to know when to stop the main menu music
        self.playMusic("main_menu.wav", "sound.menu_music_volume")

    def onEnterScene(self):
        super().onEnterScene()

        # If the player returns from the game, instead from a submenu, set again the menu music
        if self._startGame:
            self._startGame = False
            self.playMusic("main_menu.wav", "sound.menu_music_volume")

    def onExitScene(self):
        super().onExitScene()

        if self._startGame:
            pygame.mixer.music.stop()

    def onStartGame(self):
        """
        Initiate the game
        """

        self._startGame = True
        phase1 = PhaseTest()
        Director().push(phase1)

    def onOpenConfigurationMenu(self):
        """
        Edit the configuration of the game
        """

        confMenu = SettingsMenu()
        Director().push(confMenu)
