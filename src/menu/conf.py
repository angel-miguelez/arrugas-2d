# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.mouse
import sys

from conf.configuration import ConfManager

from menu.menu import Menu


class ConfMenu(Menu):
    """
    Class which holds the configuration menu and allows the user to edit it
    """

    def __init__(self, director):
        super().__init__(director, "Configuration menu")

        self._conf = ConfManager()  # get the instance of the ConfManager

        self._bindings = {}  # mapping from the configuration field name to its value e.g. {"player.movement.up" : "w"}
        self._dynamicButtonsBinds = {}  # mapping from the configuration field name to the button object
        self._dynamicButtonsTitle = {}  # mapping from the configuration field name to the button title

        self._loadPlayerMovementBindings()  # load the player movement bindings and create buttons to edit them

        self._menu.add.button('return', self._director.pop)  # button to return to the main menu

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
                    self._director.pop()
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
            self._dynamicButtonsBinds[fieldName] = self._menu.add.button(f"Move {bind}: '{keyName}'", self._editBinding,
                                                                         fieldName)
            self._dynamicButtonsTitle[fieldName] = f"Move {bind}: "
