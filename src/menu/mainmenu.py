# -*- coding: utf-8 -*-

import pygame.mouse
import pygame_menu

from conf.metainfo import MetainfoManager
from game.director import Director
from menu.settings import SettingsMenu
from menu.menu import Menu

from phase.history import SceneDialog1, SceneDialog2

backgroundColorText = (100,100,100)

class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self):
        super().__init__("Arrugas")

        self._menu.add.button('Continue', self.onStartGame,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0), selection_color=(0, 0, 0))  # button to start the game
        self._menu.add.button('Configuration', self.onOpenConfigurationMenu,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0), selection_color=(0, 0, 0))  # button to edit the configuration
        self._menu.add.button('Quit', pygame_menu.events.EXIT,
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0), selection_color=(0, 0, 0))  # button to exit the game

        self._startGame = False  # flag to know when to stop the main menu music
        self.playMusic("main_menu2.wav", "sound.menu_music_volume")

    def onEnterScene(self):
        super().onEnterScene()

        # If the player returns from the game, instead from a submenu, set again the menu music
        if self._startGame:
            self._startGame = False
            self.playMusic("main_menu2.wav", "sound.menu_music_volume")

    def onExitScene(self):
        super().onExitScene()

        if self._startGame:
            pygame.mixer.music.stop()

    def onStartGame(self):
        """
        Initiate the game
        """

        self.playMusic("button2.wav", "sound.menu_music_volume")
        self._startGame = True
        Director().push(SceneDialog2() if MetainfoManager.isTutorialDone() else SceneDialog1(), fade=True)

    def onOpenConfigurationMenu(self):
        """
        Edit the configuration of the game
        """

        confMenu = SettingsMenu()
        Director().push(confMenu)
