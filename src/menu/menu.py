# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame.mouse
import pygame_menu

from conf.configuration import ConfManager
from game.scene import Scene
from game.phase import PhaseTest


class Menu(Scene):
    """
    Abstract class which holds the basic attributes and methods of a menu
    """

    def __init__(self, director, title, **kwargs):
        super().__init__(director, title)

        # Every menu has a menu object
        self._menu = pygame_menu.Menu(title, 400, 300, theme=pygame_menu.themes.THEME_BLUE, **kwargs)

    def events(self, events):

        for event in events:

            # In every menu we can return to the previous menu with K_ESCAPE
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
                self._director.pop()

        self._menu.update(events)

    def update(self, *args):
        pass

    def draw(self, surface):
        self._menu.draw(surface)

    def onEnter(self):
        pygame.mouse.set_visible(True)

    def onExit(self):
        pass


class MainMenu(Menu):
    """
    Class which holds the main menu of the game
    """

    def __init__(self, director):
        super().__init__(director, "Main menu")

        self._menu.add.button('Play', self.onStartGame)  # button to start the game
        self._menu.add.button('Configuration', self.onOpenConfigurationMenu)  # button to edit the configuration
        self._menu.add.button('Quit', pygame_menu.events.EXIT)  # button to exit the game

    def onStartGame(self):
        """
        Initiate the game
        """

        phase1 = PhaseTest(self._director)
        self._director.push(phase1)

    def onOpenConfigurationMenu(self):
        """
        Edit the configuration of the game
        """

        confMenu = ConfMenu(self._director)
        self._director.push(confMenu)


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

    def _editBinding(self, fieldName):
        """
        Method to edit the binding with name 'fieldName'. Notice that the configuration is saved after
        the menu is left.
        """

        assigned = False  # flag to indicate that the user has assigned a key to the binding

        while not assigned:  # wait until the user assigns a key
            events = pygame.event.get()

            for event in events:

                # If the user decides to go back to the main menu
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
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
        Method to load the player movement bindings and create a button to edit each of them
        """

        for bind in ["up", "down", "right", "left"]:
            fieldName = "player.movement." + bind
            keyName = self._conf.getBind(fieldName, code=False)

            self._bindings[f"{fieldName}"] = keyName
            self._dynamicButtonsBinds[fieldName] = self._menu.add.button(f"Move {bind}: '{keyName}'", self._editBinding, fieldName)
            self._dynamicButtonsTitle[fieldName] = f"Move {bind}: "

    def onExit(self):
        super().onExit()
        self._conf.save()  # save all the bindings in the configuration file
