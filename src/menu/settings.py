# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.mouse
import sys

from conf.configuration import ConfManager
from game.director import Director

from menu.menu import Menu


backgroundColorText = (100, 100, 100)

class SettingsMenu(Menu):
    """
    Class which holds the configuration menu and allows the user to edit it
    """

    def __init__(self):
        super().__init__("Settings")

        self._conf = ConfManager()  # get the instance of the ConfManager

        self._bindings = {}  # mapping from the configuration field name to its value e.g. {"player.movement.up" : "w"}
        self._dynamicButtonsBinds = {}  # mapping from the configuration field name to the button object
        self._dynamicButtonsTitle = {}  # mapping from the configuration field name to the button title

        self._loadPlayerMovementBindings()  # load the player movement bindings and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self._loadVolumeSettings()  # load the music and sound effects volumes and create buttons to edit them
        self._menu.add.vertical_margin(30)
        self.returnButton = self._menu.add.button('return', Director().pop, background_color = backgroundColorText)  # button to return to the main menu


    def onExitScene(self):
        super().onExitScene()
        self._conf.save()  # save all the bindings in the configuration file

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
            self._dynamicButtonsBinds[fieldName] = self._menu.add.button(f"Move {bind}: '{keyName}'", self._editBinding, fieldName, background_color = backgroundColorText)
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
                                    onchange=self._editVolume, field="sound.menu_music_volume", background_color = backgroundColorText)

        gameVolume = int(float(ConfManager.getValue("sound.game_music_volume") * 100))
        self._menu.add.range_slider('Game volume', gameVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.game_music_volume", background_color = backgroundColorText)

        soundEffectsVolume = int(float(ConfManager.getValue("sound.sound_effects_volume") * 100))
        self._menu.add.range_slider('Sound effects volume', soundEffectsVolume, (0, 100), 1,
                                    value_format=lambda x: str(int(x)),
                                    onchange=self._editVolume, field="sound.sound_effects_volume", background_color = backgroundColorText)
