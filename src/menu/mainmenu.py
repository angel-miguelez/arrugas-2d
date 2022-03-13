# -*- coding: utf-8 -*-

import pygame.mouse
from pygame.locals import *
import pygame_menu

import sys

from pygame_menu.events import MenuAction

from conf.configuration import ConfManager
from conf.metainfo import MetainfoManager
from game.director import Director
from menu.menu import Menu

from phase.history import SceneDialog2, Tutorial

backgroundColorText = (100, 100, 100)


class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self):
        super().__init__("Arrugas")

        self._menu.add.button('New game', self.onStartGame, button_id="start",
                              font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0), selection_color=(0, 0, 0))  # button to start the game
        settingsSubMenu = SettingsMenu(self._menu.get_theme())
        self._menu.add.button('Configuration', SettingsMenu(self._menu.get_theme())._menu,
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
        Director().push(SceneDialog2() if MetainfoManager.isTutorialDone() else Tutorial(), fade=True)


class BackAction(MenuAction):

    def __init__(self, conf):
        super().__init__(0)
        conf.save()

    def __eq__(self, other: 'MenuAction') -> bool:
        if isinstance(other, MenuAction):
            return self._action == other._action
        return False


class SettingsMenu:
    """
    Class which holds the configuration submenu and allows the user to edit it
    """

    def __init__(self, theme):

        self._conf = ConfManager()  # get the instance of the ConfManager

        self._bindings = {}  # mapping from the configuration field name to its value e.g. {"player.movement.up" : "w"}
        self._dynamicButtonsBinds = {}  # mapping from the configuration field name to the button object
        self._dynamicButtonsTitle = {}  # mapping from the configuration field name to the button title

        self._menu = pygame_menu.Menu("Settings", 800, 600, theme=theme)
        self._loadPlayerMovementBindings()  # load the player movement bindings and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self._loadVolumeSettings()  # load the music and sound effects volumes and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self.returnButton = self._menu.add.button('return', self.saveAndReturn, self._menu, self._conf,
                                                  font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0),
                                                  selection_color=(0, 0, 0))  # button to return to the main menu

    def saveAndReturn(self, menu, conf):
        conf.save()
        menu.reset(1)

    def _editBinding(self, fieldName):
        """
        Edits the binding with name 'fieldName'. Notice that the configuration is saved after
        the menu is left.
        """

        assigned = False  # flag to indicate that the user has assigned a key to the binding

        while not assigned:  # wait until the user assigns a key
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # If the user decides to go back to the main menu
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    Director().pop()
                    return

                # If the user presses a key, then it is assigned
                elif event.type == KEYDOWN:

                    # Get the code and the name of the key
                    keyCode = event.key
                    keyName = pygame.key.name(keyCode)

                    # Update the text of the button
                    text = f"{self._dynamicButtonsTitle[fieldName]}'{keyName}'"
                    self._dynamicButtonsBinds[fieldName].set_title(text)

                    # Update the configuration
                    self._conf.setBind(fieldName, keyCode)

                    assigned = True  # exit the loop

    def _loadPlayerMovementBindings(self):
        """
        Loads the player movement bindings and creates a button to edit each of them
        """

        for bind in ["up", "down", "right", "left"]:
            fieldName = "player.movement." + bind
            keyName = self._conf.getBind(fieldName, code=False)

            self._bindings[f"{fieldName}"] = keyName
            self._dynamicButtonsBinds[fieldName] = self._menu.add.button(f"Move {bind}: '{keyName}'", self._editBinding, fieldName,
                                                                         font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0),
                                                                         selection_color=(0, 0, 0))
            self._dynamicButtonsTitle[fieldName] = f"Move {bind}: "

    def _editVolume(self, value, field):
        """
        Updates the configuration value of the volume field given
        """
        value = round(float(value) / 100, 2)
        ConfManager.setValue(field, value)

        if field == "sound.menu_music_volume":
            pygame.mixer.music.set_volume(value)

    def _loadVolumeSettings(self):
        """
        Loads the volume settings and creates a button to edit each of them
        """

        menuVolume = int(float(ConfManager.getValue("sound.menu_music_volume") * 100))
        self._menu.add.range_slider('Menu volume', menuVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.menu_music_volume",
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0),
                                    selection_color=(0, 0, 0))

        gameVolume = int(float(ConfManager.getValue("sound.game_music_volume") * 100))
        self._menu.add.range_slider('Game volume', gameVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.game_music_volume",
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0),
                                    selection_color=(0, 0, 0))

        soundEffectsVolume = int(float(ConfManager.getValue("sound.sound_effects_volume") * 100))
        self._menu.add.range_slider('Sound effects volume', soundEffectsVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.sound_effects_volume",
                                    font_shadow=True, font_shadow_offset=1, font_shadow_color=(200, 30, 0),
                                    selection_color=(0, 0, 0))